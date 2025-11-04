function ai_command
    set input (commandline)
    set tmpfile (mktemp)

    # Save original command line in case of error
    set original_input $input

    # Clear current line (visual cleanup)
    printf "\r\033[K" >&2

    # Start model in background (non-buffered)
    stdbuf -oL -eL bash -c "echo \"$input\" | ~/Documents/ShellGen/bin/python3 ~/Documents/ShellGen/shellgen.py --no-confirm > '$tmpfile' 2>&1" &
    set model_pid $last_pid

    # Spinner animation (external Bash process)
    bash -c '
        spin="/ - \\ |"
        printf "\033[?25l"   # hide cursor
        printf "[AI] Generating command... " >&2
        while kill -0 '"$model_pid"' 2>/dev/null; do
            for c in $spin; do
                kill -0 '"$model_pid"' 2>/dev/null || break
                printf "\r[AI] Generating command... %s" "$c" >&2
                sleep 0.1
            done
        done
        printf "\r[AI] Done!\033[K\n" >&2
        printf "\033[?25h"   # show cursor again
    ' &

    set spinner_pid $last_pid

    # Wait for model to finish
    wait $model_pid 2>/dev/null

    # Kill spinner (if still running)
    kill $spinner_pid 2>/dev/null

    # Read model output
    set output (cat $tmpfile)
    rm $tmpfile

    # Cleanup spinner output line
    printf "\r\033[K" >&2

    # If no output, restore user’s original text
    if test -z "$output"
        printf "[AI] Error: No output from model.\n" >&2
        commandline -r $original_input
        commandline -f repaint
        return
    end

    # Replace command line with AI-generated output
    commandline -r $output
    commandline -f repaint
end
