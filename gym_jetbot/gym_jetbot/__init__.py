from gym.envs.registration import register
 
register(
    id='JetBot-v0',
    entry_point='gym_jetbot.envs:JetBotEnv',
)