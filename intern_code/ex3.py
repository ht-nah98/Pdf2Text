def check_winner(coins):
    max_coin = max(coins)
    print(max_coin)
    coins_result = [False] * (max_coin + 1)
    coins_result[0] = False
    for coin in coins:
        if coin <= 3:
            coins_result[coin] = True
            print(coins_result)
            continue
        for i in range(1, coin + 1):
            if i - 1 >= 0 and not coins_result[i - 1]:
                coins_result[i] = True
                print('a')
            elif i - 2 >= 0 and not coins_result[i - 2]:
                coins_result[i] = True
                print('b')
            elif i - 3 >= 0 and not coins_result[i - 3]:
                coins_result[i] = True
                print('c')
            print('------------', i)
        print(coins_result)
    return [coins_result[coin] for coin in coins]

def check_game(T, coins):
    if len(coins) == T:
        return check_winner(coins)
    else:
        return check_winner(coins[:T])

T = 3
coins = [10]
results = check_game(T, coins)
for result in results:
    print(result)
