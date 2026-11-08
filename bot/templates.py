LK_URL = "https://lk.etu.ru/student#/announcements/inbox"
RC_URL = "https://student-chat.moevm.pro/"

def formatting_RK_message(
    chat: str,
    author: str,
    text: str,
    date: str,
):
    chat_name = chat
    
    if chat == "CS_6346":
        chat_name = "cs-6346"
    elif chat == "PR_6346":
        chat_name = "pr-6346"
    elif chat == "INFA":
        chat_name = "Информатика-и-ИТ-2026"
    elif chat == "PROG":
        chat_name = "Программирование-2026"
    
    content = (f'<tg-emoji emoji-id="5260268501515377807">📣</tg-emoji> <b>{chat_name}</b>\n'
                   f'<tg-emoji emoji-id="5260399854500191689">👤</tg-emoji> <i>{author}</i>\n\n'
                   f"<blockquote>{text}</blockquote>\n\n" 
                   f'<tg-emoji emoji-id="5260730055880876557">⛓️</tg-emoji> <a href="RC_URL">рокет-чат</a>')
        
    return {"text": content, "parse_mode": "HTML"} 

def formatting_LK_announcements(
    theme: str,
    author: str,
    text: str,
    date: str,
):
    if author == False or author == "None":
        author = "Неизвестный автор"
    
    content = ( f'<tg-emoji emoji-id="5260268501515377807">📣</tg-emoji> <b>{theme}</b>\n'
               f'<tg-emoji emoji-id="5260399854500191689">👤</tg-emoji> <i>{author}</i>\n\n'
               f"<blockquote>{text}</blockquote>\n\n" 
               f'<tg-emoji emoji-id="5260730055880876557">⛓️</tg-emoji> <a href="LK_URL">уведы в лк</a>' )
    
    return {"text": content, "parse_mode": "HTML"}             
