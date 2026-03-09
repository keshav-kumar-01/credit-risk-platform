const cp = require('child_process');
const p = cp.spawn('npx.cmd', [
    '-y', 'mcp-remote', 'https://stitch.googleapis.com/mcp',
    '--header', 'X-Goog-Api-Key: AQ.Ab8RN6INM7BWKgxxR6h9UpigowVEHqsOkRCmen_aQyOLdDTdyQ'
], { shell: true });

p.stderr.on('data', d => {
    console.error("STDERR:", d.toString());
});

const req = {
    jsonrpc: '2.0',
    id: 1,
    method: 'tools/call',
    params: {
        name: 'create_project',
        arguments: {
            title: 'Credit Risk Platform Redesign'
        }
    }
};
p.stdin.write(JSON.stringify(req) + '\r\n');

setTimeout(() => process.exit(0), 10000);
