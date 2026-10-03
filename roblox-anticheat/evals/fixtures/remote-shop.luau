-- Existing server-side shop. Inventory.Grant yields and can fail; it grants only if true is returned.
-- Existing economy uses leaderstats.Coins, an IntValue; no persistence changes requested.
-- Sword costs 100 Coins each. No legitimate client sends a price required by the server.
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Inventory = require(game.ServerScriptService.Inventory)
local BuyItem = ReplicatedStorage:WaitForChild("BuyItem")

BuyItem.OnServerEvent:Connect(function(player, itemId, quantity, clientPrice)
    local coins = player.leaderstats.Coins
    local total = clientPrice * quantity
    if coins.Value >= total then
        Inventory.Grant(player, itemId, quantity)
        coins.Value -= total
    end
end)
