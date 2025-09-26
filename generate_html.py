# generate_html.py (适配最终版极简表头)
import pandas as pd
import os
from urllib.parse import quote_plus
import html
import sys

# --- 全局配置 ---
CONFIG = {
    "csv_path": "project_data.csv",
    "output_dir": "dist",
    "output_filename": "index.html",
    "repo_url": "https://github.com/Lab4AI-Hub/ProjectHub",
    "issue_template": "project_application.yml" # 确保这是您项目申请的Issue模板名
}

def create_github_issue_url(title):
    base_url = f"{CONFIG['repo_url']}/issues/new"
    template = CONFIG['issue_template']
    encoded_title = quote_plus(f"[任务申请] {title}")
    return f"{base_url}?template={template}&title={encoded_title}"

def generate_html_from_csv(df):
    html_rows = []
    for index, row in df.iterrows():
        try:
            # --- 严格按照您的最终表头读取数据 ---
            project_title = html.escape(str(row.get('项目名称', '')))
            tech_tags = html.escape(str(row.get('技术标签', '')))
            project_link = str(row.get('项目原始链接', ''))
            status = str(row.get('认领状态', ''))

            # 将技术栈字符串处理成漂亮的code标签
            tech_html = "".join([f"<code>{tech.strip()}</code> " for tech in tech_tags.split(',') if tech.strip()])
            
            action_button_html = ""
            if status == '待认领':
                claim_url = create_github_issue_url(project_title)
                action_button_html = f'<a href="{claim_url}" class="claim-btn" target="_blank">📝 申请任务</a>'
            else:
                action_button_html = f'<span class="status-claimed">{status}</span>'

            html_rows.append(f"""
            <tr>
                <td><strong>{project_title}</strong></td>
                <td>{tech_html}</td>
                <td><a href="{project_link}" target="_blank">查看详情</a></td>
                <td>{action_button_html}</td>
            </tr>
            """)
        except Exception as e:
            print(f"警告：处理第 {index + 2} 行数据时发生错误: {e}")
            continue
    
    return "".join(html_rows)

def main():
    print("脚本开始运行...")
    try:
        df = pd.read_csv(CONFIG['csv_path'], encoding='utf-8-sig')
        df = df.fillna('')
        print(f"成功读取 {CONFIG['csv_path']} 文件，共 {len(df)} 条记录。")
    except Exception as e:
        print(f"读取CSV文件时发生致命错误: {e}。脚本终止。")
        sys.exit(1)

    table_content = generate_html_from_csv(df)
    
    html_template = f"""
    <!DOCTYPE html><html lang="zh-CN"><head>
        <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Lab4AI 待复现项目清单</title>
        <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.13.6/css/jquery.dataTables.min.css">
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; margin: 0; padding: 1em; background-color: #f6f8fa; }}
            .container {{ max-width: 95%; margin: 0 auto; background-color: #fff; padding: 2em; border: 1px solid #d0d7de; border-radius: 8px; }}
            header {{ text-align: center; margin-bottom: 2em; }}
            table.dataTable thead th {{ background-color: #f6f8fa; }}
            .claim-btn {{ background-color: #238636; color: white; padding: 8px 16px; text-decoration: none; border-radius: 6px; font-weight: bold; white-space: nowrap; }}
            .status-claimed {{ font-weight: bold; color: #57606a; }}
            div.dataTables_wrapper {{ width: 100%; margin: 0 auto; overflow-x: auto; }}
            code {{ background-color: rgba(175, 184, 193, 0.2); border-radius: 6px; padding: 0.2em 0.4em; font-size: 85%; margin: 0 0.2em; }}
        </style>
    </head><body>
        <div class="container">
            <header>
                <h1>Lab4AI 待复现项目清单</h1>
                <p>在申请任务前，请务必仔细阅读我们的 <a href="https://github.com/Lab4AI-Hub/ProjectHub/blob/main/WORKFLOW.md" target="_blank">贡献流程</a>。</p>
            </header>
            <table id="projectTable" class="display" style="width:100%">
                <thead><tr>
                    <th style="width: 60%;">项目名称</th>
                    <th>技术标签</th>
                    <th>原始链接</th>
                    <th>状态 / 操作</th>
                </tr></thead>
                <tbody>{table_content}</tbody>
            </table>
        </div>
        <script src="https://code.jquery.com/jquery-3.7.0.js"></script>
        <script src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js"></script>
        <script>
            $(document).ready(function() {{ $('#projectTable').DataTable({{ "pageLength": 15, "order": [], "language": {{ "search": "🔍 搜索:", "lengthMenu": "每页显示 _MENU_ 条", "info": "显示第 _START_ 到 _END_ 条，共 _TOTAL_ 条", "paginate": {{ "next": "下一页", "previous": "上一页" }} }} }}); }});
        </script>
    </body></html>
    """
    
    # ... (main函数的其余部分保持不变) ...
    output_dir = CONFIG['output_dir']
    if not os.path.exists(output_dir): os.makedirs(output_dir)
    output_path = os.path.join(output_dir, CONFIG['output_filename'])
    with open(output_path, 'w', encoding='utf-8') as f: f.write(html_template)
    print(f"网页已成功生成到: {output_path}")

if __name__ == '__main__': main()
