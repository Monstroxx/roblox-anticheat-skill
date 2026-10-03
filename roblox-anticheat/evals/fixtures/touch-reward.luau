-- Server Script under a static pickup Part. Grants 10 Coins once per current round/player.
-- Players may touch it with several body parts. Game has no approved teleport ability here.
-- Part is anchored in the supplied scene; do not change normal character movement.
local Players = game:GetService("Players")
local pickup = script.Parent

pickup.Touched:Connect(function(hit)
    local player = Players:GetPlayerFromCharacter(hit.Parent)
    if player then
        local coins = player:FindFirstChild("leaderstats")
            and player.leaderstats:FindFirstChild("Coins")
        if coins then
            coins.Value += 10
        end
    end
end)

-- Existing server RoundService changes pickup attribute RoundId each round.
-- It sets pickup attribute Active=true while rewards are eligible, false otherwise.
