import pandas as pd
from scholarly import scholarly

# List of Google Scholar IDs for this assignment
scholar_ids = [
    "hgwfis4AAAAJ",  # Example ID, replace with actual IDs
]

# List to store extracted data
data = []

for scholar_id in scholar_ids:
    try:
        author = scholarly.search_author_id(scholar_id)
        author = scholarly.fill(author)  # Get full profile details
        
        # Extract relevant details
        profile_data = {
            "Scholar ID": scholar_id,
            "Name": author.get("name", "N/A"),
            "Affiliation": author.get("affiliation", "N/A"),
            "Email": author.get("email_domain", "N/A"),
            "Citations": author["citedby"] if "citedby" in author else "N/A",
            "H-Index": author["hindex"] if "hindex" in author else "N/A",
            "i10-Index": author["i10index"] if "i10index" in author else "N/A",
            "Interests": ", ".join(author.get("interests", [])),
            "Profile URL": f"https://scholar.google.com/citations?user={scholar_id}"
        }
        data.append(profile_data)

    except Exception as e:
        print(f"Error retrieving data for ID {scholar_id}: {e}")

# Convert data to DataFrame and save to CSV
df = pd.DataFrame(data)
df.to_csv("google_scholar_profiles.csv", index=False)

print("CSV file created successfully: google_scholar_profiles.csv")
