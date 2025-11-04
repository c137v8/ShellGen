# ~/.shellgen/ai_command.sh
ai_command() {
    local input="${READLINE_LINE}"
    local tmpfile
    tmpfile=$(mktemp)

    # Run ShellGen in the background
    (echo "$input" | shellgen --no-confirm > "$tmpfile") &
    local pid=$!

    # Spinner animation
    local spin='|/-\\'
    local i=0
    tput civis
    echo -n "[AI] Generating command... "
    while kill -0 $pid 2>/dev/null; do
        printf "\b${spin:i++%${#spin}:1}"
        sleep 0.1
    done
    wait $pid 2>/dev/null
    tput cnorm
    echo -e "\r[AI] Done!        "

    local output
    output=$(<"$tmpfile")
    rm -f "$tmpfile"

    READLINE_LINE="$output"
    READLINE_POINT=${#READLINE_LINE}
}
bind -x '"\C-x\C-t": ai_command'
