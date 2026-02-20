const http = require('http')
const WebSocket = require('ws')
const setupWSConnection = require('y-websocket/bin/utils').setupWSConnection
const { checkPermission } = require('../rbac/auth')

const port = process.env.PORT || 1234
const server = http.createServer((request, response) => {
  response.writeHead(200, { 'Content-Type': 'text/plain' })
  response.end('Y.js Collaboration Server')
})

const wss = new WebSocket.Server({ server })

wss.on('connection', (conn, req) => {
  // In a real implementation, we would extract the user role from headers or tokens
  const userRole = req.headers['x-user-role'] || 'viewer';
  const project = req.url.slice(1); // Assume URL is /project-id

  console.log(`Connection request for project: ${project} with role: ${userRole}`);

  if (checkPermission(userRole, 'read')) {
    setupWSConnection(conn, req)
  } else {
    console.log('Permission denied');
    conn.close();
  }
})

server.listen(port)

console.log(`Listening to http://localhost:${port}`)
