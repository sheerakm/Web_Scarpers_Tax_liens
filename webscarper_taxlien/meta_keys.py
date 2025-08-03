from datetime import datetime

Dates = {
    "Auction Title": None,
    "Auction Start": None,
    "Auction End": None,
    "Last Day to Redeem Property": None,
    "First Day to Register": None,
    "Last Day to Register": None,
    "Last Day to Deposit Funds": None,
    "Final Day to Pay-Off Purchased Properties": None
}

def convert_date_keys(original, key_map,  ):

    key_map = {
        'Auction Title': 'Auction Title',
        'Start': 'Auction Start',
        'End': 'Auction End',
        'Last day to redeem property': 'Last Day to Redeem Property',
        'First day to register': 'First Day to Register',
        'Last day to register': 'Last Day to Register',
        'Last day to open auction trust account or deposit funds': 'Last Day to Deposit Funds',
        'Final day to pay-off properties purchased at auction': 'Final Day to Pay-Off Purchased Properties'
    }

    # Remap the dictionary
    remapped = {new_key: original[old_key] for old_key, new_key in key_map.items()}

    # Optional: fill in missing keys from Dates template if needed


    # Update Dates with remapped values
    Dates.update(remapped)

    return Dates

