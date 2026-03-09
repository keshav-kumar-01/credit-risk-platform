import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";
import fs from 'fs';

async function run() {
    const transport = new StdioClientTransport({
        command: "npx.cmd",
        args: ["-y", "mcp-remote", "https://stitch.googleapis.com/mcp", "--header", "X-Goog-Api-Key: AQ.Ab8RN6INM7BWKgxxR6h9UpigowVEHqsOkRCmen_aQyOLdDTdyQ"]
    });

    const client = new Client(
        {
            name: "test-client",
            version: "1.0.0"
        },
        {
            capabilities: {}
        }
    );

    try {
        await client.connect(transport);
        console.log("Connected");

        const projectName = "Credit Risk Platform Redesign";
        const res = await client.callTool({
            name: "create_project",
            arguments: {
                title: projectName
            }
        });

        console.log(JSON.stringify(res, null, 2));
        fs.writeFileSync('stitch_create_result.json', JSON.stringify(res, null, 2));

        // Next: Generate screen from text
        const projectId = res.content.find(c => c.text)?.text; // Or parse projectId differently
        fs.writeFileSync('stitch_project.json', JSON.stringify({ projectId }));

    } catch (e) {
        console.error(e);
    } finally {
        process.exit(0);
    }
}

run();
