import tweepy
from datetime import datetime

# Twitter API credentials - Replace these with your actual credentials
api_key = 'YOUR_API_KEY'
api_secret = 'YOUR_API_SECRET'
access_token = 'YOUR_ACCESS_TOKEN'
access_token_secret = 'YOUR_ACCESS_TOKEN_SECRET'

def authenticate(api_key, api_secret, access_token, access_token_secret):
    """Authenticate to Twitter API using Tweepy."""
    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth, wait_on_rate_limit=True)

def count_retweets(api):
    """Count the total number of retweets in the user's timeline."""
    retweets = []
    for status in tweepy.Cursor(api.user_timeline).items():
        if hasattr(status, 'retweeted_status'):
            retweets.append(status)
    return retweets

def display_retweets(retweets):
    """Display the retweets with an index number."""
    for index, status in enumerate(retweets):
        print(f"{index + 1}: [{status.created_at}] {status.text[:50]}... (ID: {status.id})")
    print(f"\nTotal retweets: {len(retweets)}\n")

def delete_retweets_by_range(api, retweets, start_index, end_index):
    """Delete retweets within the specified index range."""
    successful_deletions = 0
    failed_deletions = 0

    for status in retweets[start_index-1:end_index]:
        try:
            api.destroy_status(status.id)
            print(f"[{datetime.now()}] Deleted retweet from {status.created_at}: {status.id}")
            successful_deletions += 1
        except Exception as e:
            print(f"[{datetime.now()}] Failed to delete retweet: {status.id}, Error: {str(e)}")
            failed_deletions += 1

    print_summary(successful_deletions, failed_deletions)

def delete_retweets(api):
    """Delete all retweets."""
    successful_deletions = 0
    failed_deletions = 0

    for status in tweepy.Cursor(api.user_timeline).items():
        if hasattr(status, 'retweeted_status'):  # Check if it's a retweet
            try:
                api.destroy_status(status.id)
                print(f"[{datetime.now()}] Deleted retweet: {status.id}")
                successful_deletions += 1
            except Exception as e:
                print(f"[{datetime.now()}] Failed to delete retweet: {status.id}, Error: {str(e)}")
                failed_deletions += 1
    
    print_summary(successful_deletions, failed_deletions)

def delete_retweets_by_date(api, start_date, end_date):
    """Delete retweets within a date range."""
    successful_deletions = 0
    failed_deletions = 0

    for status in tweepy.Cursor(api.user_timeline).items():
        if hasattr(status, 'retweeted_status'):
            tweet_date = status.created_at
            if start_date <= tweet_date <= end_date:
                try:
                    api.destroy_status(status.id)
                    print(f"[{datetime.now()}] Deleted retweet from {tweet_date}: {status.id}")
                    successful_deletions += 1
                except Exception as e:
                    print(f"[{datetime.now()}] Failed to delete retweet: {status.id}, Error: {str(e)}")
                    failed_deletions += 1

    print_summary(successful_deletions, failed_deletions)

def delete_retweets_by_keyword(api, keyword):
    """Delete retweets containing a specific keyword."""
    successful_deletions = 0
    failed_deletions = 0

    for status in tweepy.Cursor(api.user_timeline).items():
        if hasattr(status, 'retweeted_status') and keyword.lower() in status.text.lower():
            try:
                api.destroy_status(status.id)
                print(f"[{datetime.now()}] Deleted retweet with keyword '{keyword}': {status.id}")
                successful_deletions += 1
            except Exception as e:
                print(f"[{datetime.now()}] Failed to delete retweet: {status.id}, Error: {str(e)}")
                failed_deletions += 1

    print_summary(successful_deletions, failed_deletions)

def delete_retweets_by_username(api, username):
    """Delete retweets from a specific username."""
    successful_deletions = 0
    failed_deletions = 0

    for status in tweepy.Cursor(api.user_timeline).items():
        if hasattr(status, 'retweeted_status') and status.retweeted_status.user.screen_name.lower() == username.lower():
            try:
                api.destroy_status(status.id)
                print(f"[{datetime.now()}] Deleted retweet from {username}: {status.id}")
                successful_deletions += 1
            except Exception as e:
                print(f"[{datetime.now()}] Failed to delete retweet: {status.id}, Error: {str(e)}")
                failed_deletions += 1

    print_summary(successful_deletions, failed_deletions)

def print_summary(successful_deletions, failed_deletions):
    """Print a summary of the deletion results."""
    print("\n==== Deletion Summary ====")
    print(f"Successful deletions: {successful_deletions}")
    print(f"Failed deletions: {failed_deletions}")
    print("==========================\n")

def main():
    # Authenticate to Twitter
    api = authenticate(api_key, api_secret, access_token, access_token_secret)
    
    # Choose an option
    print("Twitter Retweet Deletion Tool")
    print("1. Scan and display retweets")
    print("2. Delete all retweets")
    print("3. Delete retweets by date range")
    print("4. Delete retweets by keyword")
    print("5. Delete retweets by username")
    
    choice = input("Enter your choice (1-5): ")

    if choice == '1':
        # Scan the profile for retweets and display them
        retweets = count_retweets(api)
        display_retweets(retweets)
        
        if len(retweets) == 0:
            print("No retweets found on this account.")
            return

        # Prompt the user for deletion range
        try:
            start_index = int(input(f"Enter the starting index for deletion (1-{len(retweets)}): "))
            end_index = int(input(f"Enter the ending index for deletion ({start_index}-{len(retweets)}): "))
            if start_index < 1 or end_index > len(retweets) or start_index > end_index:
                print("Invalid range. Please try again.")
                return

            # Delete the specified range of retweets
            delete_retweets_by_range(api, retweets, start_index, end_index)
        except ValueError:
            print("Invalid input. Please enter numeric values.")
        
    elif choice == '2':
        delete_retweets(api)
    elif choice == '3':
        start_date_str = input("Enter start date (YYYY-MM-DD): ")
        end_date_str = input("Enter end date (YYYY-MM-DD): ")
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            delete_retweets_by_date(api, start_date, end_date)
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
    elif choice == '4':
        keyword = input("Enter keyword: ")
        delete_retweets_by_keyword(api, keyword)
    elif choice == '5':
        username = input("Enter username: ")
        delete_retweets_by_username(api, username)
    else:
        print("Invalid choice! Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()
