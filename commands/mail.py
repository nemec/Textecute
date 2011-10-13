import subprocess as sp

# Requires the program curl to be installed
def execute(arg = ''):
    if not cmd_op.has_key('MAIL_USER') or not cmd_op.has_key('MAIL_PASS'):
      return "Error: username/password not provided in settings file."
    user = cmd_op["MAIL_USER"]
    pas = cmd_op["MAIL_PASS"]
    cmd ="curl -u "+user+":"+pas+" --silent \"https://mail.google.com/mail/feed/atom\" | tr -d '\n' | awk -F '<entry>' '{for (i=2; i<=NF; i++) {print $i}}' | sed -n \"s/<title>\\(.*\)<\\/title.*name>\\(.*\\)<\\/name>.*/\\2 - \\1/p\""
    p = sp.Popen(cmd, stdout = sp.PIPE, stderr = sp.PIPE, shell = True)
    out, err = p.communicate()
    if out == "":
      out="No mail."
    if len(out) == 0:
        return err
    return out
