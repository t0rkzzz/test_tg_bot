SELECT n.id, n.text, u.telegram_id
FROM bot.note n
JOIN bot."user" u ON n.user_id = u.id
WHERE NOT n.notification_sent
AND n.text is not null
AND n.reminder_time <= $1