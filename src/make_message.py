def make_message(
            token_name,
            ca,
            ticker_name,
            marketcap,
            holders_number,
            holder_change4h,
            holder_change12h,
            holder_change1d,
            holder_change3d,
            holder_change7d):

    message = {
        "embeds": [
            {
                "title": f"-----{token_name} UPDATE-----",
                "url": f"https://dexscreener.com/solana/{ca}",
                "description": "",
                "color": 0x00FF00,  # Green color in hexadecimal
                "thumbnail": {
                    "url": f"https://dd.dexscreener.com/ds-data/tokens/solana/{ca}.png?size=lg&key=10b30e"  #get token image 
                },
                "image": {
                    "url": f"https://dd.dexscreener.com/ds-data/tokens/solana/{ca}/header.png?key=10b30e"  #get token banner on dexscreener
                },
                "fields": [
                    {
                        "name": "TICKER",
                        "value": f"{ticker_name}",
                        "inline": False
                    },
                    {
                        "name": "MCAP:",
                        "value": f"{marketcap}",
                        "inline": False
                    },
                    {
                        "name": "HOLDERS",
                        "value": f"{holders_number}",
                        "inline": False
                    },
                    {
                        "name": "------------------",
                        "value": "HOLDER CHANGES",
                        "inline": False
                    },
                    {
                        "name": "------------------",
                        "value": "",
                        "inline": False
                    },
                    {
                        "name": "4h changes",
                        "value": f"{holder_change4h}",
                        "inline": True
                    },
                    {
                        "name": "12h changes",
                        "value": f"{holder_change12h}",
                        "inline": True
                    },
                    {
                        "name": "1D changes",
                        "value": f"{holder_change1d}",
                        "inline": True
                    },
                    {
                        "name": "3D changes",
                        "value": f"{holder_change3d}",
                        "inline": True
                    },
                    {
                        "name": "7D changes",
                        "value": f"{holder_change7d}",
                        "inline": True
                    }
                ]
            }
        ]
    }

    return message
