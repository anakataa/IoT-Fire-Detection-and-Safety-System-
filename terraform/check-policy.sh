#!/bin/bash
# Script to check allowed regions in Azure Policy

echo "Finding policy assignment for 'Allowed resource deployment regions'..."
echo ""

# Get all policy assignments and filter for the one we need
ASSIGNMENT=$(az policy assignment list --scope /subscriptions/141f0972-40ad-45cd-afae-709aa76643b8 --query "[?contains(displayName, 'Allowed resource deployment') || contains(displayName, 'allowed location')].{Name:name, DisplayName:displayName}" -o json)

echo "Policy assignments found:"
echo "$ASSIGNMENT" | jq -r '.[] | "Name: \(.Name)\nDisplayName: \(.DisplayName)\n"'

echo ""
echo "Trying to get parameters for each assignment..."
for NAME in $(echo "$ASSIGNMENT" | jq -r '.[].Name'); do
    echo ""
    echo "Checking assignment: $NAME"
    az policy assignment show --name "$NAME" --scope /subscriptions/141f0972-40ad-45cd-afae-709aa76643b8 --query "parameters" -o json 2>/dev/null || echo "Could not retrieve parameters"
done

