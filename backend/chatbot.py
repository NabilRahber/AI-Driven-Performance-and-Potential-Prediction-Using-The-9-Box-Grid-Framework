"""
Chatbot module — Generates personalized improvement advice
based on the employee's 9-box grid position.
Uses a rich template-based system for each grid cell.
"""

ADVICE_TEMPLATES = {
    "Bad Hire": {
        "summary": "This employee shows low performance and low potential.",
        "advice": [
            "🔍 **Conduct a Performance Review**: Schedule an immediate one-on-one meeting to discuss specific performance gaps and set clear, measurable expectations.",
            "📋 **Create a Performance Improvement Plan (PIP)**: Define concrete goals with deadlines (30/60/90 days). Include weekly check-ins to monitor progress.",
            "🎯 **Role Alignment Check**: Evaluate whether this employee is in the right role. Sometimes poor performance stems from a mismatch between skills and job requirements.",
            "📚 **Provide Foundational Training**: Invest in basic skills training — communication, time management, and core job competencies.",
            "🤝 **Assign a Mentor**: Pair them with a high-performing peer who can provide guidance and support.",
            "⚠️ **Evaluate Fit**: If no improvement is seen after 90 days on the PIP, consider whether this role or organization is the right fit.",
        ],
    },
    "Up or Out - Grinder": {
        "summary": "This employee has moderate potential but is currently underperforming.",
        "advice": [
            "💡 **Identify Motivation Blockers**: Conduct a stay interview to understand what's demotivating them. Are there personal issues, lack of resources, or unclear expectations?",
            "🎯 **Set Stretch Goals**: Assign slightly challenging tasks that leverage their potential. Success on these will build momentum.",
            "📖 **Invest in Skill Development**: Recommend specific courses or certifications that align with their growth areas.",
            "🔄 **Rotate Responsibilities**: Expose them to different projects or teams to reignite engagement.",
            "📊 **Track Progress Closely**: Establish bi-weekly check-ins with specific KPIs to measure improvement.",
            "🌟 **Recognize Small Wins**: Acknowledge improvements, no matter how small, to build confidence and motivation.",
        ],
    },
    "Rough Diamond": {
        "summary": "This employee has high potential but isn't performing well yet — a true diamond in the rough!",
        "advice": [
            "🚀 **Fast-Track Development**: This person has raw talent. Invest heavily in coaching and development programs.",
            "🎓 **Provide Advanced Training**: Enroll them in leadership development or specialized technical training programs.",
            "👥 **Assign a Senior Mentor**: Connect them with a senior leader who can help channel their potential into performance.",
            "🎯 **Set Clear Performance Expectations**: Their potential is there; help them understand exactly what 'great performance' looks like in their role.",
            "💬 **Regular Feedback Sessions**: Provide frequent, constructive feedback. They need to know what's working and what's not.",
            "🔀 **Expose to High-Visibility Projects**: Give them opportunities to shine on important projects where they can prove themselves.",
        ],
    },
    "Talent Risk": {
        "summary": "This employee performs at a medium level but shows limited growth potential.",
        "advice": [
            "🔒 **Retention Focus**: Ensure they're satisfied in their current role since their solid performance is valuable.",
            "📈 **Lateral Development**: Since vertical growth may be limited, explore lateral moves that keep them engaged.",
            "🏆 **Recognize Contributions**: Regularly acknowledge their steady, reliable performance.",
            "📝 **Knowledge Documentation**: Leverage their experience — have them document processes and train newer team members.",
            "💰 **Competitive Compensation**: Ensure their pay reflects their contribution to reduce flight risk.",
            "🎯 **Specialized Skill Building**: Help them become a deep expert in their current domain.",
        ],
    },
    "Core Player": {
        "summary": "This is a solid, steady contributor with moderate performance and potential.",
        "advice": [
            "📊 **Expand Responsibilities**: Gradually increase scope to test and develop their capabilities.",
            "🎓 **Cross-Training**: Expose them to adjacent roles or departments to broaden their skill set.",
            "🤝 **Peer Leadership**: Assign them as a team lead on small projects to develop leadership skills.",
            "💬 **Career Conversations**: Have regular discussions about their aspirations and create a development roadmap.",
            "🏅 **Performance Incentives**: Tie bonuses or recognition to measurable performance improvements.",
            "📚 **Continuous Learning**: Encourage participation in workshops, conferences, and online courses.",
        ],
    },
    "High Potential": {
        "summary": "This employee has high potential with moderate current performance — a future leader!",
        "advice": [
            "🚀 **Leadership Pipeline**: Include them in your leadership development program immediately.",
            "🎯 **Challenging Assignments**: Give them high-impact, challenging projects that push their boundaries.",
            "👔 **Executive Exposure**: Provide opportunities to present to senior leadership and gain visibility.",
            "📋 **Create an Individual Development Plan (IDP)**: Outline specific competencies to develop over 6-12 months.",
            "🌍 **Cross-Functional Projects**: Assign them to cross-department initiatives to build broader business acumen.",
            "🎓 **Sponsor External Education**: Support MBA, certifications, or executive education programs.",
        ],
    },
    "Solid Performer": {
        "summary": "This employee delivers high performance but shows limited growth potential.",
        "advice": [
            "🏆 **Celebrate Excellence**: Publicly recognize their consistent high performance. They are the backbone of the team.",
            "🎯 **Deepen Expertise**: Help them become the go-to subject matter expert in their domain.",
            "📖 **Mentoring Role**: Leverage their expertise by having them mentor junior team members.",
            "💰 **Reward Performance**: Ensure compensation and benefits reflect their high contribution.",
            "🔧 **Process Improvement**: Engage them in optimizing workflows and processes — they know the work best.",
            "⚖️ **Work-Life Balance**: Monitor for burnout since high performers can overextend themselves.",
        ],
    },
    "High Performer": {
        "summary": "This employee excels in performance and shows solid growth potential.",
        "advice": [
            "⭐ **Key Talent Recognition**: Identify them as key talent in your succession planning.",
            "🎯 **Stretch Assignments**: Continuously provide challenging work that matches their growing capabilities.",
            "🌟 **Visibility Opportunities**: Ensure senior leadership knows who they are — sponsor their visibility.",
            "📈 **Accelerated Career Path**: Create a clear, accelerated career trajectory with milestones.",
            "💼 **Strategic Projects**: Involve them in strategic initiatives that impact the bottom line.",
            "🤝 **Retention Strategy**: Develop a strong retention plan — these employees are highly sought after by competitors.",
        ],
    },
    "Star": {
        "summary": "🌟 This is your STAR employee — top performance AND top potential!",
        "advice": [
            "🏅 **Succession Planning**: This employee should be on your succession plan for critical leadership roles.",
            "🚀 **Executive Track**: Fast-track them into the leadership pipeline with executive coaching.",
            "💎 **Premium Retention Package**: Offer competitive compensation, equity, and growth opportunities to retain them.",
            "🌍 **Global/Cross-Functional Leadership**: Give them enterprise-wide responsibilities and exposure.",
            "🎤 **Thought Leadership**: Encourage them to represent the company at industry events and conferences.",
            "⚡ **Innovation Projects**: Assign them to lead innovation or transformation initiatives.",
            "👑 **Empower Decision Making**: Give them autonomy and authority — trust breeds loyalty and growth.",
        ],
    },
}


def generate_advice(grid_label: str, employee_name: str, prediction_details: dict) -> list:
    """
    Generate chatbot messages with improvement advice.
    Returns a list of message objects.
    """
    template = ADVICE_TEMPLATES.get(grid_label, ADVICE_TEMPLATES["Core Player"])

    messages = []

    # First message: Overview
    messages.append({
        "role": "assistant",
        "content": f"## 📊 Analysis for {employee_name}\n\n"
                   f"**9-Box Position:** {grid_label}\n"
                   f"**Performance Level:** {prediction_details.get('performance', 'Medium')}\n"
                   f"**Potential Level:** {prediction_details.get('potential', 'Medium')}\n"
                   f"**Model Used:** {prediction_details.get('model_used', 'Best Model')}\n\n"
                   f"{template['summary']}"
    })

    # Second message: Improvement advice
    advice_text = f"## 💡 Improvement Recommendations for {employee_name}\n\n"
    advice_text += "Here's a personalized development plan based on their current 9-box position:\n\n"
    for item in template["advice"]:
        advice_text += f"- {item}\n"

    messages.append({
        "role": "assistant",
        "content": advice_text,
    })

    return messages


def chat_response(user_message: str, grid_label: str, employee_name: str) -> str:
    """
    Generate a contextual response to user follow-up questions about the employee.
    """
    template = ADVICE_TEMPLATES.get(grid_label, ADVICE_TEMPLATES["Core Player"])
    msg_lower = user_message.lower()

    if any(word in msg_lower for word in ["training", "learn", "course", "skill"]):
        return (
            f"For **{employee_name}** (currently: {grid_label}), I'd recommend focusing on:\n\n"
            f"- Online courses on platforms like Coursera, LinkedIn Learning, or Udemy\n"
            f"- Internal mentorship programs\n"
            f"- Hands-on project-based learning\n"
            f"- Industry certifications relevant to their role\n\n"
            f"The key is to align training with the specific gaps identified in their performance review."
        )

    if any(word in msg_lower for word in ["promote", "promotion", "advance", "career"]):
        return (
            f"Regarding **{employee_name}**'s career advancement (currently: {grid_label}):\n\n"
            f"- **Performance**: {template['summary']}\n"
            f"- Before considering promotion, ensure they consistently meet or exceed current expectations\n"
            f"- Create a clear career development plan with measurable milestones\n"
            f"- Consider lateral moves if vertical promotion isn't immediately suitable"
        )

    if any(word in msg_lower for word in ["retain", "retention", "keep", "lose"]):
        return (
            f"To retain **{employee_name}** ({grid_label}):\n\n"
            f"- Ensure competitive compensation and benefits\n"
            f"- Provide meaningful work and growth opportunities\n"
            f"- Foster a positive team culture\n"
            f"- Regular check-ins to understand their satisfaction\n"
            f"- Recognize and celebrate their contributions"
        )

    # Default response
    return (
        f"Based on **{employee_name}**'s position as **{grid_label}**:\n\n"
        f"{template['summary']}\n\n"
        f"Key focus areas:\n"
        + "\n".join(f"- {a}" for a in template["advice"][:3])
        + "\n\nWould you like to know more about specific areas like training, promotion paths, or retention strategies?"
    )
