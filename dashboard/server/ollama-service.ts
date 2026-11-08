import { randomUUID } from 'crypto'
import type { ConversationActivity } from '../src/types/conversations'
import type {
  ConversationExecutionHandle,
  ConversationExecutor,
  ConversationExecutorRequest,
  ConversationExecutorResult,
} from './conversation-manager'
import { ConversationExecutionError } from './conversation-manager'

export interface OllamaStatus {
  available: boolean
  host: string
  model: string
  models: string[]
  error: string | null
}

let cachedStatus: { status: OllamaStatus; timestamp: number } | null = null
const CACHE_TTL_MS = 4_000

export async function getOllamaStatus(
  customHost?: string,
  customModel?: string,
): Promise<OllamaStatus> {
  const host = customHost || process.env.OLLAMA_HOST || 'http://127.0.0.1:11434'
  const targetModel = customModel || process.env.OLLAMA_MODEL || 'lfm2.5-thinking:1.2b'

  const now = Date.now()
  if (cachedStatus && now - cachedStatus.timestamp < CACHE_TTL_MS) {
    return cachedStatus.status
  }

  try {
    const controller = new AbortController()
    const timeout = setTimeout(() => controller.abort(), 2_000)
    const response = await fetch(`${host}/api/tags`, {
      method: 'GET',
      signal: controller.signal,
    })
    clearTimeout(timeout)

    if (!response.ok) {
      const status: OllamaStatus = {
        available: false,
        host,
        model: targetModel,
        models: [],
        error: `Ollama HTTP ${response.status}`,
      }
      cachedStatus = { status, timestamp: now }
      return status
    }

    const data = (await response.json()) as { models?: Array<{ name?: string }> }
    const installedModels = (data.models || [])
      .map((m) => m.name || '')
      .filter(Boolean)

    const hasTarget = installedModels.some(
      (name) => name === targetModel || name.startsWith(`${targetModel}:`),
    )
    const activeModel = hasTarget
      ? targetModel
      : installedModels[0] || targetModel

    const status: OllamaStatus = {
      available: true,
      host,
      model: activeModel,
      models: installedModels,
      error: null,
    }
    cachedStatus = { status, timestamp: now }
    return status
  } catch (err) {
    const status: OllamaStatus = {
      available: false,
      host,
      model: targetModel,
      models: [],
      error: err instanceof Error ? err.message : String(err),
    }
    cachedStatus = { status, timestamp: now }
    return status
  }
}

export function createOllamaConversationExecutor(
  customModel?: string,
  customHost?: string,
): ConversationExecutor {
  const host = customHost || process.env.OLLAMA_HOST || 'http://127.0.0.1:11434'
  const configuredModel = customModel || process.env.OLLAMA_MODEL || 'lfm2.5-thinking:1.2b'

  return (request: ConversationExecutorRequest, onActivity: (activity: ConversationActivity) => void): ConversationExecutionHandle => {
    let cancelled = false
    const controller = new AbortController()

    const result = new Promise<ConversationExecutorResult>(async (resolvePromise, rejectPromise) => {
      onActivity({ kind: 'analyzing', label: `Analyzing deal with Ollama (${configuredModel})` })

      try {
        const response = await fetch(`${host}/api/chat`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          signal: controller.signal,
          body: JSON.stringify({
            model: configuredModel,
            messages: [{ role: 'user', content: request.prompt }],
            format: 'json',
            stream: false,
            options: {
              temperature: 0.2,
            },
          }),
        })

        if (!response.ok) {
          const errorText = await response.text()
          throw new ConversationExecutionError(
            `Ollama returned HTTP ${response.status}: ${errorText}`,
            'ollama_error',
            true,
          )
        }

        onActivity({ kind: 'answering', label: 'Preparing verified specialist answer' })

        const data = (await response.json()) as { message?: { content?: string } }
        const rawContent = data.message?.content || '{}'
        
        let parsed: Record<string, unknown>
        try {
          parsed = JSON.parse(rawContent.trim()) as Record<string, unknown>
        } catch {
          const match = rawContent.match(/```(?:json)?\s*([\s\S]*?)```/i)?.[1]
          if (match) {
            parsed = JSON.parse(match.trim()) as Record<string, unknown>
          } else {
            throw new ConversationExecutionError('Ollama returned invalid JSON response.', 'invalid_response', true)
          }
        }

        resolvePromise({
          sessionId: request.expectedSessionId || randomUUID(),
          response: parsed,
        })
      } catch (err) {
        if (cancelled) {
          rejectPromise(new ConversationExecutionError('The conversation turn was cancelled.', 'cancelled', true))
          return
        }
        rejectPromise(
          new ConversationExecutionError(
            err instanceof Error ? err.message : String(err),
            'ollama_failed',
            true,
          ),
        )
      }
    })

    return {
      result,
      cancel: () => {
        cancelled = true
        controller.abort()
      },
    }
  }
}
