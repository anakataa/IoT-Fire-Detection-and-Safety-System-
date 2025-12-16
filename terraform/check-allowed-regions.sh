#!/bin/bash
# Script to check which Azure regions are allowed for your subscription

echo "Checking available regions for your Azure subscription..."
echo ""

# Try to get list of regions (requires Azure CLI)
if command -v az &> /dev/null; then
    echo "Available regions (this may take a moment):"
    az account list-locations --query "[].{Name:name, DisplayName:displayName}" -o table
    echo ""
    echo "NOTE: Even if a region appears in this list, your subscription policy may still restrict it."
    echo "To check allowed regions, go to Azure Portal > Subscriptions > Your Subscription > Resource Providers"
else
    echo "Azure CLI not found. Please install it or check Azure Portal:"
    echo "1. Go to Azure Portal (https://portal.azure.com)"
    echo "2. Navigate to: Subscriptions > Your Subscription > Resource Providers"
    echo "3. Or check: Subscriptions > Your Subscription > Settings > Allowed regions"
fi

