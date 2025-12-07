#!/bin/bash
set -e

echo "=== Knowledge Vault Upload Test Script ==="
echo

# 1. Clean up any lingering Node processes
echo "Step 1: Cleaning up Node processes..."
ps aux 2>/dev/null | grep -E "node.*next" | grep -v grep | awk '{print $2}' | xargs -r kill 2>/dev/null || true
sleep 2

# 2. Start Next.js dev server in background
echo "Step 2: Starting Next.js dev server..."
npm run dev > /tmp/next-test.log 2>&1 &
NEXT_PID=$!
echo "Next.js PID: $NEXT_PID"

# 3. Wait for server to be ready
echo "Step 3: Waiting for server to start..."
for i in {1..15}; do
  if curl -s http://localhost:3000/ > /dev/null 2>&1; then
    echo "Server is ready!"
    break
  fi
  echo -n "."
  sleep 1
done
echo

# 4. Test upload via API
echo "Step 4: Testing upload via /api/vault/upload..."
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST http://localhost:3000/api/vault/upload \
  -H "x-internal-user-id: test-user-cli" \
  -F "file=@/tmp/kv-test.txt" \
  -F "title=CLI Upload Test" \
  -F "notes=Testing upload API proxy")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)

echo "HTTP Status: $HTTP_CODE"
echo "Response Body: $BODY"
echo

# 5. Check database
echo "Step 5: Checking database for new record..."
node scripts/checkDocs.js | tail -10
echo

# 6. Show Next.js logs
echo "Step 6: Last 20 lines of Next.js logs..."
tail -20 /tmp/next-test.log
echo

# 7. Cleanup
echo "Step 7: Stopping Next.js server (PID $NEXT_PID)..."
kill $NEXT_PID 2>/dev/null || true
wait $NEXT_PID 2>/dev/null || true

echo
echo "=== Test Complete ==="
