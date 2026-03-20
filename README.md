<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mohammed Desouky – Data Analytics Dashboard Profile</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            background: linear-gradient(145deg, #f4f7fc 0%, #eef2f5 100%);
            font-family: 'Segoe UI', 'Roboto', 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Helvetica Neue', sans-serif;
            padding: 2rem;
            display: flex;
            justify-content: center;
            align-items: center;
            line-height: 1.4;
        }

        /* main dashboard container */
        .dashboard {
            max-width: 1400px;
            width: 100%;
            background: #ffffff;
            border-radius: 32px;
            box-shadow: 0 20px 35px -12px rgba(0, 0, 0, 0.08), 0 1px 2px rgba(0, 0, 0, 0.02);
            overflow: hidden;
            transition: all 0.2s ease;
        }

        /* header like BI top bar */
        .dashboard-header {
            background: #ffffff;
            padding: 1.5rem 2rem 0.8rem 2rem;
            border-bottom: 1px solid #e9edf2;
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            align-items: flex-end;
        }

        .title-section h1 {
            font-size: 1.85rem;
            font-weight: 700;
            background: linear-gradient(135deg, #1C2B3E, #2C4A6E);
            background-clip: text;
            -webkit-background-clip: text;
            color: transparent;
            letter-spacing: -0.3px;
        }

        .title-section p {
            color: #5b6e8c;
            font-weight: 500;
            font-size: 1rem;
            margin-top: 6px;
        }

        .header-badge {
            background: #f0f4f9;
            padding: 8px 16px;
            border-radius: 40px;
            font-size: 0.8rem;
            font-weight: 500;
            color: #1e466e;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }

        /* filter simulation row */
        .filter-bar {
            padding: 1rem 2rem;
            background: #fafcff;
            border-bottom: 1px solid #eef2f8;
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            align-items: center;
        }

        .filter-chip {
            background: white;
            border: 1px solid #dfe4ea;
            border-radius: 40px;
            padding: 0.4rem 1rem;
            font-size: 0.8rem;
            font-weight: 500;
            color: #2c3e50;
            cursor: default;
            transition: all 0.2s;
            box-shadow: 0 1px 1px rgba(0,0,0,0.02);
        }

        .filter-chip:hover {
            background: #eef3fc;
            border-color: #7f9bc0;
            transform: translateY(-1px);
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.03);
        }

        .filter-label {
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: #6f8fae;
        }

        /* KPI row (cards) */
        .kpi-row {
            display: flex;
            flex-wrap: wrap;
            gap: 1.5rem;
            padding: 2rem 2rem 0.5rem 2rem;
        }

        .kpi-card {
            background: #ffffff;
            flex: 1 1 200px;
            border-radius: 28px;
            padding: 1.2rem 1rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.02), 0 1px 2px rgba(0, 0, 0, 0.03);
            border: 1px solid #eef2f8;
            transition: all 0.25s ease;
        }

        .kpi-card:hover {
            transform: translateY(-3px);
            border-color: #cddfed;
            box-shadow: 0 15px 25px -12px rgba(0, 20, 40, 0.1);
        }

        .kpi-label {
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.4px;
            color: #6783a3;
        }

        .kpi-value {
            font-size: 2.2rem;
            font-weight: 800;
            color: #1f3b4c;
            line-height: 1.2;
            margin: 8px 0 4px;
        }

        .kpi-trend {
            font-size: 0.7rem;
            color: #4791a3;
            font-weight: 500;
        }

        /* two column layout */
        .dashboard-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.8rem;
            padding: 1.5rem 2rem 2rem 2rem;
        }

        /* card widget style */
        .widget-card {
            background: #ffffff;
            border-radius: 28px;
            border: 1px solid #eef2f8;
            padding: 1.3rem 1.4rem;
            margin-bottom: 1.8rem;
            transition: box-shadow 0.2s;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.02);
        }

        .widget-card:hover {
            box-shadow: 0 12px 24px -12px rgba(0, 0, 0, 0.08);
            border-color: #e0e8f0;
        }

        .widget-title {
            font-size: 1rem;
            font-weight: 700;
            color: #1e3a5f;
            border-left: 4px solid #5f9bc2;
            padding-left: 12px;
            margin-bottom: 1.2rem;
            letter-spacing: -0.2px;
        }

        .skills-chips {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            margin-top: 8px;
        }

        .skill-badge {
            background: #f2f6fb;
            border-radius: 32px;
            padding: 8px 16px;
            font-weight: 600;
            font-size: 0.85rem;
            color: #1e466e;
            transition: all 0.2s;
            border: 1px solid #e2e9f1;
        }

        .skill-badge:hover {
            background: #e5f0fe;
            transform: scale(1.02);
        }

        .project-card {
            border-bottom: 1px solid #f0f4fa;
            padding: 1rem 0;
        }

        .project-card:last-child {
            border-bottom: none;
        }

        .project-title {
            font-weight: 800;
            color: #1e3a5f;
            display: flex;
            gap: 12px;
            align-items: baseline;
            flex-wrap: wrap;
        }

        .project-tools {
            font-size: 0.7rem;
            font-weight: 500;
            background: #eef3fc;
            padding: 2px 8px;
            border-radius: 30px;
            color: #2c6280;
        }

        .project-impact {
            font-size: 0.85rem;
            color: #3d5a73;
            margin-top: 6px;
            line-height: 1.4;
        }

        .core-list {
            display: flex;
            flex-wrap: wrap;
            gap: 14px;
            margin-top: 6px;
        }

        .core-item {
            background: #f9fbfe;
            padding: 6px 14px;
            border-radius: 24px;
            font-size: 0.8rem;
            font-weight: 500;
            color: #2c4b6e;
        }

        .github-stats {
            background: #fafcff;
            border-radius: 24px;
            padding: 0.8rem;
            text-align: center;
            font-size: 0.85rem;
            border: 1px solid #eef2f8;
        }

        .social-links {
            display: flex;
            gap: 18px;
            justify-content: center;
            margin-top: 18px;
        }

        .social-icon {
            text-decoration: none;
            font-weight: 500;
            color: #2b6a9f;
            font-size: 0.85rem;
            background: #eef3fc;
            padding: 6px 15px;
            border-radius: 40px;
            transition: 0.2s;
        }

        .social-icon:hover {
            background: #deeaf6;
            transform: translateY(-2px);
        }

        hr {
            margin: 0.5rem 0;
            border-color: #eef2f8;
        }

        @media (max-width: 800px) {
            .dashboard-grid {
                grid-template-columns: 1fr;
                padding: 1rem;
            }
            .kpi-row {
                padding: 1rem;
            }
            body {
                padding: 1rem;
            }
        }
    </style>
</head>
<body>
<div class="dashboard">
    <!-- header area: dashboard style -->
    <div class="dashboard-header">
        <div class="title-section">
            <h1>📊 DATA ANALYTICS DASHBOARD</h1>
            <p>Mohammed Desouky · Senior Data Analyst | Turning Data into Decisions</p>
        </div>
        <div class="header-badge">
            🧠 Live BI Profile · v2.4
        </div>
    </div>

    <!-- slicer simulation / filters -->
    <div class="filter-bar">
        <span class="filter-label">🔍 FILTERS (SIMULATION):</span>
        <div class="filter-chip">📅 Last 12 months</div>
        <div class="filter-chip">🏢 All Projects</div>
        <div class="filter-chip">📊 Dashboard View: Executive</div>
        <div class="filter-chip">⭐ Top Skills</div>
    </div>

    <!-- KPI METRICS row (dashboard KPIs) -->
    <div class="kpi-row">
        <div class="kpi-card">
            <div class="kpi-label">📁 TOTAL PROJECTS</div>
            <div class="kpi-value">14</div>
            <div class="kpi-trend">▲ +3 this year</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">📊 DASHBOARDS BUILT</div>
            <div class="kpi-value">50+</div>
            <div class="kpi-trend">enterprise-grade BI</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">⚡ DATA PROCESSED</div>
            <div class="kpi-value">2.1M</div>
            <div class="kpi-trend">rows analyzed · 1M+ content records</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">🛠️ TOOLS MASTERED</div>
            <div class="kpi-value">9</div>
            <div class="kpi-trend">Power BI · SQL · Python · Excel · R</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">📈 REPORT ACCURACY</div>
            <div class="kpi-value">97%</div>
            <div class="kpi-trend">executive trust index</div>
        </div>
    </div>

    <!-- main grid: left + right widgets -->
    <div class="dashboard-grid">
        <!-- LEFT COLUMN -->
        <div>
            <!-- About me - premium -->
            <div class="widget-card">
                <div class="widget-title">📌 ABOUT ME — DATA STORYTELLER</div>
                <p style="color: #2c4a6e; font-weight: 500; margin-bottom: 10px;">"I don't just work with data — I build systems that make data speak the language of business."</p>
                <p style="color: #3a5a78; font-size: 0.9rem; line-height: 1.5;">Senior Data Analyst based in New Cairo, Egypt. I transform ambiguous business questions into precise, evidence-backed decisions using <strong>Power BI, SQL, Python, Excel & R</strong>. Experience across KPMG, Tata Group, Accenture global simulations. I build dashboards non-technical executives actually trust & use daily.</p>
                <div style="margin-top: 16px; display: flex; gap: 10px; flex-wrap: wrap;">
                    <span style="background:#eef2fa; border-radius:20px; padding:4px 12px;">🎯 Strategic KPI design</span>
                    <span style="background:#eef2fa; border-radius:20px; padding:4px 12px;">📖 Data storytelling</span>
                    <span style="background:#eef2fa; border-radius:20px; padding:4px 12px;">🤖 AI-assisted analytics</span>
                </div>
            </div>

            <!-- Dashboard Skills Section (cards style) -->
            <div class="widget-card">
                <div class="widget-title">📊 CORE DASHBOARD SKILLS</div>
                <div class="skills-chips">
                    <div class="skill-badge">📈 Power BI (Expert)</div>
                    <div class="skill-badge">🐍 Python (Pandas, NumPy)</div>
                    <div class="skill-badge">🔍 SQL (Complex queries)</div>
                    <div class="skill-badge">📑 Excel & Power Query</div>
                    <div class="skill-badge">📊 Tableau Fundamentals</div>
                    <div class="skill-badge">📐 R / Statistical Analysis</div>
                </div>
            </div>

            <!-- featured projects (dashboard widgets) -->
            <div class="widget-card">
                <div class="widget-title">📂 FEATURED PROJECTS — IMPACT DASHBOARDS</div>
                <div class="project-card">
                    <div class="project-title">🎯 Customer Segmentation Dashboard <span class="project-tools">Power BI · RFM</span></div>
                    <div class="project-impact">📍 KPMG Virtual Experience: RFM analysis on large customer dataset. Identified top 20% customers driving 80% revenue. Informed high-churn retention strategy.</div>
                </div>
                <div class="project-card">
                    <div class="project-title">🌍 Revenue & Geographic Intelligence <span class="project-tools">SQL · Power BI</span></div>
                    <div class="project-impact">📍 Tata Group: Multi-region revenue heatmaps + what-if scenario planning. Reduced exec reporting prep time by <strong>70%</strong>.</div>
                </div>
                <div class="project-card">
                    <div class="project-title">📈 Content Performance Analytics <span class="project-tools">Python · SQL</span></div>
                    <div class="project-impact">📍 Accenture: Analyzed 1M+ content records, surfaced top 5 content types, driving +40% user engagement.</div>
                </div>
                <div class="project-card">
                    <div class="project-title">🏢 KPI Framework & Financial Dashboard <span class="project-tools">Power BI · Excel</span></div>
                    <div class="project-impact">Consolidated 30+ business metrics, eliminated 12 manual reports, saved 15+ hours/week across departments.</div>
                </div>
            </div>
        </div>

        <!-- RIGHT COLUMN -->
        <div>
            <!-- Core competencies +  KPI design -->
            <div class="widget-card">
                <div class="widget-title">🧠 CORE COMPETENCIES (BUSINESS INSIGHTS)</div>
                <div class="core-list">
                    <div class="core-item">🧹 Data Cleaning & QA</div>
                    <div class="core-item">📊 Data Visualization</div>
                    <div class="core-item">🎯 KPI Design & Frameworks</div>
                    <div class="core-item">💡 Business Insights Translation</div>
                    <div class="core-item">📖 Storytelling with Data</div>
                    <div class="core-item">🤖 AI-assisted Analytics</div>
                    <div class="core-item">📐 Statistical Testing</div>
                </div>
                <!-- proficiency visual simulation -->
                <div style="margin-top: 20px;">
                    <div style="display: flex; justify-content: space-between; font-size: 0.75rem;"><span>Power BI</span><span>Expert ████████████████████</span></div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.75rem; margin-top: 8px;"><span>SQL</span><span>Advanced ███████████████████░</span></div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.75rem; margin-top: 8px;"><span>Python (Pandas)</span><span>Proficient █████████████████░░░</span></div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.75rem; margin-top: 8px;"><span>Excel / Power Query</span><span>Expert ████████████████████</span></div>
                </div>
            </div>

            <!-- experience highlights - table like dashboard -->
            <div class="widget-card">
                <div class="widget-title">💼 EXPERIENCE HIGHLIGHTS</div>
                <div style="display: flex; flex-direction: column; gap: 14px;">
                    <div><strong>🏢 KPMG</strong> — Data Analytics Virtual Analyst<br><span style="font-size:0.8rem; color:#4a627a;">RFM segmentation · Marketing insights dashboard · data quality assurance</span></div>
                    <div><strong>🏢 Tata Group</strong> — BI Consultant (Virtual)<br><span style="font-size:0.8rem; color:#4a627a;">Revenue heatmaps · what-if scenario planning · KPI development for finance</span></div>
                    <div><strong>🏢 Accenture</strong> — Data Analyst (Virtual)<br><span style="font-size:0.8rem; color:#4a627a;">1M+ row content analysis · SQL + Python integration · trend forecasting</span></div>
                </div>
            </div>

            <!-- certifications + github analytics clean-->
            <div class="widget-card">
                <div class="widget-title">📜 CERTIFICATIONS & EDUCATION</div>
                <div style="display: flex; flex-direction: column; gap: 10px;">
                    <div>🎓 Data Analysis Diploma — Full lifecycle (Extract → Model → Visualize → Communicate)</div>
                    <div>✅ KPMG Data Analytics Consulting · ✅ Tata Data Visualization · ✅ Accenture Data Analytics</div>
                    <div>📍 Tools: Excel, SQL, Power BI, Python, R, Applied Statistics</div>
                </div>
                <hr style="margin: 14px 0;">
                <div class="widget-title" style="margin-bottom: 8px;">📉 GITHUB ANALYTICS</div>
                <div class="github-stats">
                    <div style="display: flex; justify-content: space-around; flex-wrap: wrap;">
                        <div>📁 Repos: 12+</div>
                        <div>⭐ Stars: focused BI projects</div>
                        <div>📊 Activity: weekly dashboard commits</div>
                    </div>
                    <div style="font-size:0.7rem; margin-top: 12px;">🚀 Featured: Power BI templates, SQL optimization scripts, Python ETL notebooks</div>
                </div>
            </div>

            <!-- social links + contact / professional footer -->
            <div class="widget-card" style="text-align: center;">
                <div class="widget-title">🌐 CONNECT & COLLABORATE</div>
                <div class="social-links">
                    <a href="https://github.com/eldep4667-gif" target="_blank" class="social-icon">🐙 GitHub</a>
                    <a href="https://www.linkedin.com/in/mohammed-desouky-a73289282/" target="_blank" class="social-icon">🔗 LinkedIn</a>
                    <a href="https://x.com/mohmad_Eldep" target="_blank" class="social-icon">𝕏 Twitter</a>
                    <a href="https://youtube.com/@aldepds?si=XeEVDTU_Q7hmGEsO" target="_blank" class="social-icon">▶️ YouTube</a>
                </div>
                <div style="margin-top: 16px; font-size:0.8rem; color:#4b6f8e;">📧 eldep4667@gmail.com · Portfolio ready for BI consulting</div>
                <div style="margin-top: 8px; font-size: 0.7rem; background: #f2f7fd; display: inline-block; padding: 5px 14px; border-radius: 20px;">⚡ “Turning data into strategic decisions”</div>
            </div>
        </div>
    </div>

    <!-- subtle footer like dashboard update -->
    <div style="padding: 0.8rem 2rem 1.5rem 2rem; border-top: 1px solid #eef2f8; font-size: 0.7rem; color:#8da0b0; text-align: center;">
        <span>📊 LIVE DATA DASHBOARD — interactive simulation · metrics based on real-world impact · last updated 2025</span>
    </div>
</div>
</body>
</html>
