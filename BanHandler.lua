--author:striving
--don't steal my code without giving me credits
local HttpService = game:GetService("HttpService")
local Players = game:GetService("Players")

local API_URL = "" 
local API_KEY = ""

local function checkifbanned(player)
    local url = string.format("%s/is_banned/%d", API_URL, player.UserId)
    local headers = {}
    if API_KEY ~= "" then
        headers["x-api-key"] = API_KEY
    end

    local success, res = pcall(function()
        return HttpService:GetAsync(url, true, headers)
    end)

    if not success then
        warn("failed to check if " .. player.Name .. "is banned")
        return
    end

    local data = HttpService:JSONDecode(res)

    if data.banned then
        local reason = nil


        if data.entry and data.entry.reason and data.entry.reason ~= "" then
            reason = data.entry.reason
        end
        --will add moderator name
        player:Kick("You are banned from this game.\nReason: " .. reason)
    end
end

Players.PlayerAdded:Connect(function(player)
    spawn(function()
        while true do --this is not the best way to check for bans but i guess it works for now, would want a way different implementations of this using something like messaging service.
        wait(1)
        checkifbanned(player)
        end
    end)
end)
