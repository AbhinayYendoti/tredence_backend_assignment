import random

def get_mock_suggestion(code: str, cursor_position: int, language: str) -> dict:
    """
    Generate a mocked autocomplete suggestion.
    This is a simple rule-based approach, not real AI.
    """
    # Get the context around cursor
    lines = code.split('\n')
    current_line_idx = code[:cursor_position].count('\n')
    current_line = lines[current_line_idx] if current_line_idx < len(lines) else ""
    
    # Get characters before cursor on current line
    col_pos = cursor_position - (code[:cursor_position].rfind('\n') + 1) if '\n' in code[:cursor_position] else cursor_position
    context = current_line[:col_pos].strip()
    
    suggestions_map = {
        "python": [
            "def ",
            "return ",
            "if ",
            "for ",
            "while ",
            "import ",
            "from ",
            "class ",
            "print(",
            "self.",
            "try:",
            "except ",
        ],
        "javascript": [
            "function ",
            "const ",
            "let ",
            "return ",
            "if ",
            "for ",
            "while ",
            "console.log(",
            "async ",
            "await ",
            "=> ",
        ],
        "java": [
            "public ",
            "private ",
            "class ",
            "void ",
            "return ",
            "if ",
            "for ",
            "while ",
            "System.out.println(",
        ]
    }
    
    suggestions = suggestions_map.get(language.lower(), suggestions_map["python"])
    
    # Check if user is typing something specific
    if context:
        # Simple pattern matching
        if context.endswith("def") or context.endswith("class"):
            suggestion = " "
        elif context.endswith("if") or context.endswith("for") or context.endswith("while"):
            suggestion = " ():"
        elif context.endswith("import"):
            suggestion = " "
        elif context.endswith("from"):
            suggestion = " import "
        else:
            # Random suggestion or common patterns
            matching_suggestions = [s for s in suggestions if s.lower().startswith(context.lower())]
            if matching_suggestions:
                suggestion = matching_suggestions[0][len(context):]
            else:
                suggestion = random.choice(suggestions) if suggestions else ""
    else:
        suggestion = random.choice(suggestions) if suggestions else ""
    
    # Calculate positions
    start_pos = cursor_position
    end_pos = cursor_position + len(suggestion)
    
    return {
        "suggestion": suggestion,
        "start_position": start_pos,
        "end_position": end_pos
    }

