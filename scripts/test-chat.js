async function test() {
  const dealId = 'parkview-2026-001';
  // 1. Create thread
  const createRes = await fetch(`http://127.0.0.1:8081/api/deals/${dealId}/conversations`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      agentId: 'rent-roll-analyst',
      title: 'Testing Ollama Response'
    })
  });
  const createData = await createRes.json();
  console.log('Created thread:', createData.thread?.threadId);
  const threadId = createData.thread.threadId;

  // 2. Post message
  const msgRes = await fetch(`http://127.0.0.1:8081/api/deals/${dealId}/conversations/${threadId}/messages`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      content: 'Tell me about this deal in one short sentence.',
      clientRequestId: 'test-' + Date.now()
    })
  });
  const msgData = await msgRes.json();
  console.log('Enqueued message turn:', msgData);

  // 3. Poll
  for (let i = 0; i < 40; i++) {
    await new Promise(r => setTimeout(r, 4000));
    const r = await fetch(`http://127.0.0.1:8081/api/deals/${dealId}/conversations/${threadId}`);
    const data = await r.json();
    console.log(`Poll ${i+1}: thread status=${data.thread?.status}, activeTurnId=${data.thread?.activeTurnId}, messages=${data.messages?.length}`);
    if (data.messages?.length > 1) {
      console.log('Assistant message:\n', JSON.stringify(data.messages[data.messages.length - 1], null, 2));
      break;
    }
  }
}
test().catch(console.error);
