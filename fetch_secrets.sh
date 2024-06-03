#!/bin/bash
gh auth login


# Repository information
OWNER="dave-b-b"
REPO="simplitrac"

# Fetch secrets from GitHub and write to .env file
echo "Fetching secrets from GitHub for $OWNER/$REPO..."

gh secret list --repo "$OWNER/$REPO" | while read -r secret_name _; do
  secret_value=$(gh secret view "$secret_name" --repo "$OWNER/$REPO" | jq -r .encrypted_value)
  echo "$secret_name=$secret_value" >> .env
done

echo ".env file created with the secrets."