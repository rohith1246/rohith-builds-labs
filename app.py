import logging
import os

from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'rbl-dev-secret-2026')

DATABASE_URL = os.environ.get('DATABASE_URL', '')
EMAIL_USER = os.environ.get('EMAIL_USER', '')
EMAIL_PASS = os.environ.get('EMAIL_PASS', '')
RECIPIENT_EMAIL = os.environ.get('RECIPIENT_EMAIL', 'rohithbuildslab@gmail.com')


# ─── Database ────────────────────────────────────────────────────────────────
import psycopg2

def get_db():
    conn = psycopg2.connect(DATABASE_URL)
    return conn


def init_db():
    if not DATABASE_URL:
        logging.warning("No DATABASE_URL set — skipping DB init.")
        return
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS inquiries (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                company VARCHAR(255),
                email VARCHAR(255),
                project_type VARCHAR(100),
                budget VARCHAR(100),
                description TEXT,
                created_at TIMESTAMP DEFAULT NOW(),
                status VARCHAR(50) DEFAULT 'new'
            )
        """)
        conn.commit()
        cur.close()
        conn.close()
        logging.info("DB initialized.")
    except Exception as e:
        logging.error(f"DB init error: {e}")


# ─── Email ───────────────────────────────────────────────────────────────────

def send_email_notification(data):
    logging.info(f"New inquiry from {data['email']} — email notifications disabled.")
    return

# ─── Routes ──────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/work')
def work():
    return render_template('work.html')


@app.route('/services')
def services():
    return render_template('services.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        data = {
            'name': request.form.get('name', '').strip(),
            'company': request.form.get('company', '').strip(),
            'email': request.form.get('email', '').strip(),
            'project_type': request.form.get('project_type', '').strip(),
            'budget': request.form.get('budget', '').strip(),
            'description': request.form.get('description', '').strip(),
        }

        # Validate required fields
        if not data['name'] or not data['email'] or not data['description']:
            flash('Please fill in all required fields.', 'error')
            return render_template('contact.html', form_data=data)

        # Save to PostgreSQL
        if DATABASE_URL:
            try:
                conn = get_db()
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO inquiries (name, company, email, project_type, budget, description)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    data['name'], data['company'], data['email'],
                    data['project_type'], data['budget'], data['description']
                ))
                conn.commit()
                cur.close()
                conn.close()
            except Exception as e:
                logging.error(f"DB insert error: {e}")

        # Send email notification (silent fallback if not configured)
        send_email_notification(data)

        flash("I'll review your project and get back within 24 hours.", 'success')
        return redirect(url_for('contact'))

    return render_template('contact.html', form_data={})


# ─── Blog ────────────────────────────────────────────────────────────────────

BLOG_POSTS = [
    {
        "slug": "why-most-ai-agents-fail-in-production",
        "title": "Why Most AI Agents Fail in Production (And How to Build Ones That Don't)",
        "date": "June 12, 2026",
        "category": "AI Engineering",
        "reading_time": "6 min read",
        "summary": "Most AI agent demos are impressive. Most AI agents in production are broken. Here's what separates the two — and how to build agents that actually work under real conditions.",
        "content": """
<p>Every week, someone posts a video of an AI agent doing something impressive. It searches the web, writes code, sends emails, books meetings. The demo is clean. The music is good. The comments are full of amazement.</p>

<p>And then you try to build something similar for a real business, and it falls apart immediately.</p>

<h2>The Demo Problem</h2>

<p>Demos are curated. The prompt is crafted. The data is clean. The API doesn't rate-limit. The model doesn't hallucinate on that particular input. The whole thing runs once, perfectly, and gets recorded.</p>

<p>Production is none of that. Production means:</p>

<ul>
<li>Users who type things the model has never seen before</li>
<li>APIs that go down at 3am</li>
<li>Rate limits that kick in at exactly the wrong time</li>
<li>Edge cases that only appear after 10,000 runs</li>
<li>State that gets corrupted when something crashes mid-task</li>
</ul>

<p>Most AI agent architectures are built to make demos work. Not to survive production.</p>

<h2>What Actually Breaks</h2>

<p><strong>1. No error recovery.</strong> The agent calls an API, gets a 429, and crashes. There's no retry logic, no exponential backoff, no fallback. The whole task fails silently.</p>

<p><strong>2. No state management.</strong> If the agent is halfway through a multi-step task and something goes wrong, it starts over. Or worse — it doesn't start over and leaves things in a broken half-state.</p>

<p><strong>3. No observability.</strong> The agent runs in a black box. When something goes wrong (and it will), you have no logs, no traces, no way to understand what happened or reproduce it.</p>

<p><strong>4. Prompt brittleness.</strong> The agent works great on the exact inputs from the demo. Change the input format slightly, add a typo, provide data in a different structure — and the whole thing breaks. The prompt was tuned for one scenario, not generalized.</p>

<h2>How to Build Agents That Survive Production</h2>

<p><strong>Build for failure first.</strong> Every external call should have retry logic. Every task should be idempotent — running it twice should be safe. Every failure should be logged with enough context to debug later.</p>

<p><strong>Make state explicit.</strong> Don't rely on the model to remember what it's done. Use a database. Write state after every step. If the agent restarts, it should be able to pick up exactly where it left off.</p>

<p><strong>Add observability from day one.</strong> Log every action, every decision, every external call. You don't need a fancy observability platform — a database table with timestamps and outcomes is enough to start.</p>

<p><strong>Test the edge cases, not just the happy path.</strong> What happens when the API returns an empty response? What happens when the model output isn't in the expected format? What happens when the task takes 10x longer than expected? These scenarios need to be handled, not hoped away.</p>

<h2>The Practical Version</h2>

<p>At Rohith Builds Labs, I've built agents that run autonomously in production — job aggregators that update daily, research agents that synthesize web sources, Reddit automation systems that queue reply drafts continuously.</p>

<p>None of them work because I found the perfect prompt. They work because I built them with failure in mind, added proper logging, handled rate limits explicitly, and designed for the actual conditions they'd run in — not the ideal conditions of a demo environment.</p>

<p>If you're building an AI agent, spend less time on the prompt and more time on the infrastructure around it. The prompt is the easy part.</p>
"""
    },
    {
        "slug": "automation-vs-ai-agents-knowing-which-to-build",
        "title": "Automation vs AI Agents: Knowing Which One to Build for Your Problem",
        "date": "June 10, 2026",
        "category": "Systems Thinking",
        "reading_time": "4 min read",
        "summary": "Not every business problem needs an AI agent. Many are better solved with simple automation. Here's how to tell the difference — and why it matters for what you build.",
        "content": """
<p>There's a tendency in the AI space right now to reach for agents as the solution to every problem. Need to send emails? AI agent. Need to update a spreadsheet? AI agent. Need to check if an order shipped? AI agent.</p>

<p>This is usually the wrong call. And it makes systems more complex, less reliable, and harder to maintain than they need to be.</p>

<h2>The Difference That Matters</h2>

<p><strong>Automation</strong> is for tasks where the steps are known in advance, the inputs are structured, and the correct output is deterministic. If you can write the logic as a flowchart with no ambiguous decision points, it's an automation problem.</p>

<p><strong>AI agents</strong> are for tasks where the steps depend on context, the inputs are unstructured or unpredictable, or the correct action requires understanding rather than just pattern-matching. If the task genuinely requires reasoning, it's an agent problem.</p>

<h2>Examples That Clarify It</h2>

<p><strong>Automation problems:</strong></p>
<ul>
<li>Send a welcome email when a user signs up</li>
<li>Move a row from "Pending" to "Complete" when payment is confirmed</li>
<li>Pull job listings from an RSS feed and insert them into a database</li>
<li>Generate a daily PDF report from database metrics</li>
</ul>

<p><strong>Agent problems:</strong></p>
<ul>
<li>Read a support ticket, understand the issue, and draft a relevant response</li>
<li>Research a company from a name alone and produce a summary with sources</li>
<li>Monitor Reddit threads and identify the ones genuinely worth engaging with</li>
<li>Given a product description, write SEO-optimized copy variations</li>
</ul>

<p>The pattern: if the task involves understanding natural language, making judgment calls, or handling genuinely unpredictable inputs — it's an agent problem. If it's a defined workflow with known inputs and outputs — it's automation.</p>

<h2>Why This Distinction Matters for What You Build</h2>

<p>Automation is cheaper, faster, more reliable, and easier to debug. If your problem is an automation problem and you build an agent for it, you've added unnecessary complexity, cost, and failure surface area.</p>

<p>Agents are more expensive to run, harder to debug, and more likely to produce unexpected outputs. If your problem is genuinely an agent problem and you try to handle it with rigid automation, it'll break on every edge case you didn't anticipate.</p>

<p>Most real systems need both. A good architecture has automation handling the structured parts of a workflow and agents handling the parts that require genuine reasoning.</p>

<h2>Start With the Simpler Thing</h2>

<p>When I scope new projects at Rohith Builds Labs, my default assumption is that automation is sufficient until proven otherwise. I look at what the task actually requires — not what sounds impressive in a pitch.</p>

<p>If the problem can be solved with a cron job and a few API calls, that's what I build. If it genuinely requires an LLM to reason through unstructured context — I build an agent, and I build it to survive production.</p>

<p>The goal is always the simplest system that solves the actual problem. Not the most technically interesting system. Not the one that makes the best demo. The one that runs reliably when you're not watching it.</p>
"""
    },
]


@app.route('/blog')
def blog():
    return render_template('blog.html', posts=BLOG_POSTS)


@app.route('/blog/<slug>')
def blog_post(slug):
    post = next((p for p in BLOG_POSTS if p['slug'] == slug), None)
    if not post:
        return render_template('blog.html', posts=BLOG_POSTS), 404
    other_posts = [p for p in BLOG_POSTS if p['slug'] != slug]
    return render_template('post.html', post=post, other_posts=other_posts)


# ─── Startup ─────────────────────────────────────────────────────────────────

with app.app_context():
    init_db()

if __name__ == '__main__':
    app.run(debug=True, port=5001)
