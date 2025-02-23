import sys

def generate_github_dork_links(filename):
    without_suffix = filename.split('.')[0]
    queries = [
        ("password", "password"),
        ("npmrc _auth", "npmrc _auth"),
        ("dockercfg", "dockercfg"),
        ("pem private", "pem private"),
        ("id_rsa", "id_rsa"),
        ("s3cfg", "s3cfg"),
        ("htpasswd", "htpasswd"),
        ("git-credentials", "git-credentials"),
        ("bashrc password", "bashrc password"),
        ("sshd_config", "sshd_config"),
        ("xoxp OR xoxb OR xoxa", "xoxp OR xoxb OR xoxa"),
        ("SECRET_KEY", "SECRET_KEY"),
        ("passwd", "passwd"),
        (".env", ".env"),
        (".exs", ".exs"),
        ("beanstalkd.yml", "beanstalkd.yml"),
        ("deploy.rake", "deploy.rake"),
        ("credentials", "credentials"),
        ("PWD", "PWD"),
        (".bash_history", ".bash_history"),
        (".sls", ".sls"),
        ("secrets", "secrets"),
        ("composer.json", "composer.json"),
        ("access_key", "access_key"),
        ("access_token", "access_token"),
        ("api_key", "api_key"),
        ("api_secret", "api_secret"),
        ("app_key", "app_key"),
        ("app_secret", "app_secret"),
        ("auth_token", "auth_token"),
        ("aws_access_key_id", "aws_access_key_id"),
        ("aws_secret", "aws_secret"),
        ("client_secret", "client_secret"),
        ("db_password", "db_password"),
        ("db_username", "db_username"),
        ("encryption_key", "encryption_key"),
        ("firebase", "firebase"),
        ("ftp", "ftp"),
        ("gh_token", "gh_token"),
        ("github_token", "github_token"),
        ("gmail_password", "gmail_password"),
        ("gmail_username", "gmail_username"),
        ("herokuapp", "herokuapp"),
        ("ldap_password", "ldap_password"),
        ("ldap_username", "ldap_username"),
        ("master_key", "master_key"),
        ("mysql", "mysql"),
        ("oauth_token", "oauth_token"),
        ("private_key", "private_key"),
        ("redis_password", "redis_password"),
        ("root_password", "root_password"),
        ("secret", "secret"),
        ("secret_access_key", "secret_access_key"),
        ("secret_token", "secret_token"),
        ("security_credentials", "security_credentials"),
        ("slack_api", "slack_api"),
        ("sql_password", "sql_password"),
        ("ssh", "ssh"),
        ("token", "token"),
        ("x-api-key", "x-api-key"),
        ("xoxb", "xoxb"),
        ("xoxp", "xoxp"),
    ]

    print("\n************ Github Dork Links (must be logged in) *******************")
    for query, description in queries:
        print(f" {description}")
        print(f"https://github.com/search?q=%22{filename}%22+{query}&type=Code")
        print(f"https://github.com/search?q=%22{without_suffix}%22+{query}&type=Code")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python dorkdeneme.py <filename>")
        sys.exit(1)
    
    filename = sys.argv[1]
    generate_github_dork_links(filename)