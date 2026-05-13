"""Prompt templates for the coaching system."""

COACH_SYSTEM_PROMPT = """你是 C++ 面试教练，擅长通过追问和场景化提问帮助用户深入理解知识点。
你需要根据用户的学习情况生成合适的面试题，并在评估时给出具体、有建设性的反馈。"""

COACH_QUESTION_PROMPT = """基于以下 context 生成面试题：
topic={topic}, difficulty={difficulty}, weakness_tags={weakness_tags}, user_mastery={user_mastery}

要求：
1. 题目难度应与 difficulty 匹配（1=基础，2=中等，3=深入）
2. 结合 weakness_tags 针对用户的薄弱点
3. 考虑 user_mastery 调整题目复杂度
4. 生成清晰、具体的面试题"""

COACH_EVALUATION_PROMPT = """你是一个 C++ 面试官，评估用户回答质量。

question: {question}
user_answer: {user_answer}
key_points: {key_points}

请以 JSON 格式返回评估结果，必须包含以下字段：
- rating: "good" | "okay" | "poor"
- score_total: 0.0-1.0 的总体评分
- correctness: 正确性 0.0-1.0
- completeness: 完整性 0.0-1.0
- depth: 深度 0.0-1.0
- clarity: 清晰度 0.0-1.0
- code_accuracy: 代码准确性 0.0-1.0
- edge_case_awareness: 边界情况意识 0.0-1.0
- missing_points: 遗漏的要点 list
- wrong_points: 错误的要点 list
- weakness_tags: 薄弱点标签 list
- hallucinated_points: 幻觉点（胡说八道的知识点）list
- evaluator_confidence: 评估置信度 0.0-1.0"""

COACH_REFERENCE_ANSWER_PROMPT = """基于以下 context 生成参考答案：
topic: {topic}
difficulty: {difficulty}
key_points: {key_points}

要求：
1. 覆盖所有 key_points
2. 难度与 difficulty 匹配
3. 包含代码示例（如果适用）
4. 解释原理和应用场景"""