import * as vscode from 'vscode';
import { spawn } from 'child_process';
import * as path from 'path';

interface Issue {
    severity: string;
    category: string;
    message: string;
    line?: number;
    suggestion?: string;
}

interface ValidationResult {
    trust_score: number;
    passed: boolean;
    categories: Record<string, { score: number; weight: number; issue_count: number }>;
    issues: Issue[];
}

let diagnosticCollection: vscode.DiagnosticCollection;
let statusBarItem: vscode.StatusBarItem;
let outputChannel: vscode.OutputChannel;

export function activate(context: vscode.ExtensionContext) {
    console.log('AI Code Trust Validator is now active');

    diagnosticCollection = vscode.languages.createDiagnosticCollection('ai-trust-validator');
    outputChannel = vscode.window.createOutputChannel('AI Trust Validator');

    // Status bar item
    statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
    statusBarItem.command = 'aiTrust.validate';
    statusBarItem.tooltip = 'Click to validate AI code';
    statusBarItem.text = '$(shield) AI Trust';
    statusBarItem.show();

    // Register commands
    context.subscriptions.push(
        vscode.commands.registerCommand('aiTrust.validate', validateWorkspace),
        vscode.commands.registerCommand('aiTrust.validateFile', validateCurrentFile),
        vscode.commands.registerCommand('aiTrust.showReport', showReport),
        vscode.commands.registerCommand('aiTrust.clearCache', clearCache),
        vscode.commands.registerCommand('aiTrust.watchMode', toggleWatchMode),
        diagnosticCollection,
        statusBarItem,
        outputChannel
    );

    // Auto-validate on save if enabled
    vscode.workspace.onDidSaveTextDocument((document) => {
        const config = vscode.workspace.getConfiguration('aiTrust');
        if (config.get('autoValidate') && document.languageId === 'python') {
            validateDocument(document);
        }
    });
}

async function validateWorkspace() {
    const workspaceFolders = vscode.workspace.workspaceFolders;
    if (!workspaceFolders) {
        vscode.window.showErrorMessage('No workspace folder open');
        return;
    }

    await vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: "🛡️ Validating AI code...",
        cancellable: false
    }, async (progress) => {
        const workspacePath = workspaceFolders[0].uri.fsPath;
        const result = await runValidation(workspacePath);
        
        if (result) {
            updateStatusBar(result.trust_score, result.passed);
            showResultNotification(result);
        }
    });
}

async function validateCurrentFile() {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        vscode.window.showErrorMessage('No active file');
        return;
    }

    const document = editor.document;
    if (document.languageId !== 'python') {
        vscode.window.showWarningMessage('AI Trust Validator currently supports Python only');
        return;
    }

    await validateDocument(document);
}

async function validateDocument(document: vscode.TextDocument): Promise<void> {
    const config = vscode.workspace.getConfiguration('aiTrust');
    const filePath = document.uri.fsPath;
    
    outputChannel.appendLine(`\n🔍 Validating: ${filePath}`);

    await vscode.window.withProgress({
        location: vscode.ProgressLocation.Window,
        title: "Validating..."
    }, async () => {
        const result = await runValidation(filePath);
        
        if (result) {
            updateStatusBar(result.trust_score, result.passed);
            
            // Update diagnostics
            const diagnostics: vscode.Diagnostic[] = result.issues.map(issue => {
                const line = (issue.line || 1) - 1;
                const range = new vscode.Range(line, 0, line, 1000);
                const severity = getSeverity(issue.severity);
                
                const diagnostic = new vscode.Diagnostic(
                    range,
                    `${issue.message}${issue.suggestion ? '\n💡 ' + issue.suggestion : ''}`,
                    severity
                );
                diagnostic.source = 'AI Trust Validator';
                diagnostic.code = issue.category;
                
                return diagnostic;
            });
            
            diagnosticCollection.set(document.uri, diagnostics);
            
            // Show notification for critical issues
            const criticalCount = result.issues.filter(i => i.severity === 'critical').length;
            if (criticalCount > 0) {
                vscode.window.showErrorMessage(
                    `🚨 ${criticalCount} critical issue${criticalCount > 1 ? 's' : ''} found in ${path.basename(filePath)}`
                );
            }
            
            outputChannel.appendLine(`📊 Trust Score: ${result.trust_score}/100`);
            outputChannel.appendLine(`   Issues: ${result.issues.length}`);
        }
    });
}

async function runValidation(targetPath: string): Promise<ValidationResult | null> {
    const config = vscode.workspace.getConfiguration('aiTrust');
    const pythonPath = config.get<string>('pythonPath', 'python');
    const minScore = config.get<number>('minScore', 70);
    const strict = config.get<boolean>('strictMode', false);

    return new Promise((resolve) => {
        const args = [
            '-m', 'ai_trust_validator.cli',
            'validate', targetPath,
            '--json',
            '--min-score', String(minScore)
        ];
        
        if (strict) {
            args.push('--strict');
        }

        const proc = spawn(pythonPath, args, {
            cwd: vscode.workspace.workspaceFolders?.[0]?.uri.fsPath
        });

        let stdout = '';
        let stderr = '';

        proc.stdout.on('data', (data) => {
            stdout += data.toString();
        });

        proc.stderr.on('data', (data) => {
            stderr += data.toString();
        });

        proc.on('close', (code) => {
            if (stderr) {
                outputChannel.appendLine(`Error: ${stderr}`);
            }
            
            try {
                const data = JSON.parse(stdout);
                resolve(data.results?.[0] || data);
            } catch {
                resolve(null);
            }
        });

        proc.on('error', (err) => {
            outputChannel.appendLine(`Failed to run validator: ${err.message}`);
            vscode.window.showErrorMessage(
                'AI Trust Validator not found. Install it with: pip install ai-trust-validator'
            );
            resolve(null);
        });
    });
}

function getSeverity(severity: string): vscode.DiagnosticSeverity {
    switch (severity) {
        case 'critical':
        case 'high':
            return vscode.DiagnosticSeverity.Error;
        case 'medium':
            return vscode.DiagnosticSeverity.Warning;
        case 'low':
            return vscode.DiagnosticSeverity.Information;
        default:
            return vscode.DiagnosticSeverity.Hint;
    }
}

function updateStatusBar(score: number, passed: boolean) {
    const icon = passed ? '$(check)' : '$(warning)';
    const color = score >= 80 ? 'green' : score >= 60 ? 'yellow' : 'red';
    
    statusBarItem.text = `${icon} Trust: ${score}/100`;
    statusBarItem.tooltip = `Trust Score: ${score}/100\n${passed ? '✓ Passed' : '✗ Failed'}\n\nClick to validate`;
    statusBarItem.backgroundColor = passed 
        ? undefined 
        : new vscode.ThemeColor('statusBarItem.warningBackground');
    statusBarItem.show();
}

function showResultNotification(result: ValidationResult) {
    const message = result.passed
        ? `✅ Trust Score: ${result.trust_score}/100 - Passed`
        : `❌ Trust Score: ${result.trust_score}/100 - Issues found`;
    
    if (result.passed) {
        vscode.window.showInformationMessage(message);
    } else {
        vscode.window.showWarningMessage(message, 'View Report').then(selection => {
            if (selection === 'View Report') {
                showReport();
            }
        });
    }
}

async function showReport() {
    const editor = vscode.window.activeTextEditor;
    if (!editor) return;

    const result = await runValidation(editor.document.uri.fsPath);
    if (!result) return;

    const panel = vscode.window.createWebviewPanel(
        'aiTrustReport',
        'AI Trust Report',
        vscode.ViewColumn.Beside,
        { enableScripts: true }
    );

    panel.webview.html = generateReportHtml(result);
}

function generateReportHtml(result: ValidationResult): string {
    const scoreColor = result.trust_score >= 80 ? '#00ff88' : 
                       result.trust_score >= 60 ? '#ffaa00' : '#ff4444';
    
    return `<!DOCTYPE html>
<html>
<head>
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            padding: 20px;
            background: #1e1e1e;
            color: #e4e4e4;
        }
        .score { 
            font-size: 72px; 
            font-weight: bold; 
            color: ${scoreColor};
            text-align: center;
        }
        .categories { margin-top: 20px; }
        .category { 
            display: flex; 
            justify-content: space-between;
            padding: 10px;
            background: rgba(255,255,255,0.05);
            margin: 5px 0;
            border-radius: 8px;
        }
        .issues { margin-top: 20px; }
        .issue {
            padding: 12px;
            background: rgba(255,255,255,0.03);
            margin: 8px 0;
            border-radius: 8px;
            border-left: 3px solid;
        }
        .critical { border-color: #ff4444; }
        .high { border-color: #ff8800; }
        .medium { border-color: #ffaa00; }
        .low { border-color: #00d9ff; }
        .suggestion { color: #00ff88; margin-top: 8px; }
    </style>
</head>
<body>
    <h1>🛡️ AI Trust Report</h1>
    <div class="score">${result.trust_score}/100</div>
    <p style="text-align: center;">${result.passed ? '✅ Passed' : '❌ Failed'}</p>
    
    <h2>Categories</h2>
    <div class="categories">
        ${Object.entries(result.categories).map(([name, data]) => `
            <div class="category">
                <span>${name}</span>
                <span>${data.score}/100</span>
            </div>
        `).join('')}
    </div>
    
    <h2>Issues (${result.issues.length})</h2>
    <div class="issues">
        ${result.issues.slice(0, 10).map(issue => `
            <div class="issue ${issue.severity}">
                <strong>[${issue.severity.toUpperCase()}]</strong> 
                ${issue.message}
                ${issue.line ? `<span style="color:#888"> (Line ${issue.line})</span>` : ''}
                ${issue.suggestion ? `<div class="suggestion">💡 ${issue.suggestion}</div>` : ''}
            </div>
        `).join('')}
    </div>
    
    <p style="margin-top: 30px; color: #666; text-align: center;">
        Generated by <a href="https://github.com/rudra496/ai-code-trust-validator">AI Code Trust Validator</a>
    </p>
</body>
</html>`;
}

async function clearCache() {
    const config = vscode.workspace.getConfiguration('aiTrust');
    const pythonPath = config.get<string>('pythonPath', 'python');
    
    spawn(pythonPath, ['-m', 'ai_trust_validator.cli', 'cache', 'clear']);
    vscode.window.showInformationMessage('AI Trust Validator cache cleared');
}

let isWatchMode = false;

function toggleWatchMode() {
    isWatchMode = !isWatchMode;
    
    if (isWatchMode) {
        vscode.window.showInformationMessage('👀 Watch mode enabled - files will validate on change');
        statusBarItem.text = '$(eye) AI Trust (watching)';
    } else {
        vscode.window.showInformationMessage('Watch mode disabled');
        statusBarItem.text = '$(shield) AI Trust';
    }
}

export function deactivate() {
    diagnosticCollection.dispose();
    statusBarItem.dispose();
    outputChannel.dispose();
}
