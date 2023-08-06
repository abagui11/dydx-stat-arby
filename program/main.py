from constants import ABORT_ALL_POSITIONS, FIND_COINTEGRATED, PLACE_TRADES, MANAGE_EXITS
from func_connections import connect_dydx
from func_private import abort_all_positions
from func_public import construct_market_prices
from func_cointegration import store_cointegration_results
from func_entry_pairs import open_positions
from func_exit_pairs import manage_trade_exits
from func_messaging import send_message


# MAIN FUNCTION
if __name__ == "__main__":

    # Message on start
    send_message("I launched")
    
    # Connect to client
    try:
        print("Connecting to Client...")
        client = connect_dydx()
    except Exception as e:
        print("Error connecting to client: ", e)
        # Send message
        send_message(f"I couldn't connect to client. {e}")
        exit(1)

    # Abort all open positions
    if ABORT_ALL_POSITIONS:
        try:
            print("Closing all positions...")
            close_orders = abort_all_positions(client)
        except Exception as e:
            print("Error closing all positions: ", e)
            # Send message
            send_message(f"I couldn't close all positions. {e}")
            exit(1)
    
    # Finding Cointegrated pairs
    if FIND_COINTEGRATED:
        
        # Construct Market prices
        try:
            print("Fetching market prices, takes a few minutes...")
            df_market_prices = construct_market_prices(client)
        except Exception as e:
            print("Error constructing market prices: ", e)
            # Send message
            send_message(f"I couldn't construct market prices. {e}")
            exit(1)

        # Store cointegrated pairs
        try:
            print("Storing cointegrated pairs...")
            stores_result = store_cointegration_results(df_market_prices)
            if stores_result != "saved":
                print("Error saving cointegrated pairs")
                exit(1)
        except Exception as e:
            print("Error saving cointegrated pairs: ", e)
            # Send message
            send_message(f"I couldn't save cointegrated pairs. {e}")
            exit(1)
    
    # Keep the bot on
    while True:

        # Place trades for opening positions
        if MANAGE_EXITS:
            try:
                print("Managing exits...")
                manage_trade_exits(client)
            except Exception as e:
                print("Error managing exiting positions: ", e)
                # Send message
                send_message(f"I couldn't manage exiting positions properly. {e}")
                exit(1)

        # Place trades for opening positions
        if PLACE_TRADES:
            try:
                print("Finding trade opportunities...")
                open_positions(client)
            except Exception as e:
                print("Error trading pairs: ", e)
                # Send message
                send_message(f"I couldn't open trades correctly. {e}")
                exit(1)
        