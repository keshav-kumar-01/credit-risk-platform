const cp = require('child_process');
const fs = require('fs');

const p = cp.spawn('npx.cmd', [
    '-y', 'mcp-remote', 'https://stitch.googleapis.com/mcp',
    '--header', 'X-Goog-Api-Key: AQ.Ab8RN6INM7BWKgxxR6h9UpigowVEHqsOkRCmen_aQyOLdDTdyQ'
], { shell: true });

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

let buffer = '';
p.stdout.on('data', d => {
    buffer += d.toString();
    if (buffer.includes('"id":1') && buffer.includes('result')) {
        fs.writeFileSync('create_out.json', buffer);
        p.kill();
        process.exit(0);
    }
});

p.stderr.on('data', d => {
    console.error(d.toString());
});

p.stdin.write(JSON.stringify(req) + '\r\n');

setTimeout(() => {
    console.error("Timeout reached");
    if (buffer) {
        fs.writeFileSync('create_out_partial.json', buffer);
    }
    p.kill();
    process.exit(1);
}, 20000);
