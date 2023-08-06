"""
The v2 environments support multi actions in one game tick, with frameskip = 0
"""


from .types import Config
import numpy as np
from . import microrts_ai

"""
WinLossRewardFunction(), 
ResourceGatherRewardFunction(),  
ProduceWorkerRewardFunction(),
ProduceBuildingRewardFunction(),
AttackRewardFunction(),
ProduceCombatUnitRewardFunction(),
CloserToEnemyBaseRewardFunction(),
reward_weight corresponds to above
"""
shaped_reward_envs = True
hrl_envs = True

envs = []

envs += [dict(
    id=f"MicrortsMining-v2",
    entry_point='gym_microrts.envs:GlobalAgentMultiActionsCombinedRewardEnv',
    kwargs=dict(
        frame_skip=0,
        ai2=microrts_ai.passiveAI,
        map_path="maps/10x10/basesTwoWorkers10x10.xml",
        reward_weight=np.array([0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    ),
    max_episode_steps=2000,
)]

envs += [dict(
    id=f"MicrortsProduceWorker-v2",
    entry_point='gym_microrts.envs:GlobalAgentMultiActionsCombinedRewardEnv',
    kwargs=dict(
        frame_skip=0,
        ai2=microrts_ai.passiveAI,
        map_path="maps/10x10/basesTwoWorkers10x10.xml",
        reward_weight=np.array([0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0])
    ),
    max_episode_steps=2000,
)]

envs += [dict(
    id=f"MicrortsAttackPassiveEnemySparseReward-v2",
    entry_point='gym_microrts.envs:GlobalAgentMultiActionsCombinedRewardEnv',
    kwargs=dict(
        frame_skip=0,
        ai2=microrts_ai.passiveAI,
        map_path="maps/10x10/basesWorkers10x10.xml",
        reward_weight=np.array([0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0])
    ),
    max_episode_steps=2000,
)]
envs += [dict(
    id=f"MicrortsProduceCombatUnitsSparseReward-v2",
    entry_point='gym_microrts.envs:GlobalAgentMultiActionsCombinedRewardEnv',
    kwargs=dict(
        frame_skip=0,
        ai2=microrts_ai.passiveAI,
        map_path="maps/10x10/basesWorkers10x10.xml",
        reward_weight=np.array([0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0])
    ),
    max_episode_steps=2000,
)]
envs += [dict(
    id="MicrortsDefeatRandomEnemySparseReward-v2",
    entry_point='gym_microrts.envs:GlobalAgentMultiActionsCombinedRewardEnv',
    kwargs=dict(
        frame_skip=0,
        ai2=microrts_ai.randomBiasedAI,
        map_path="maps/10x10/basesWorkers10x10.xml",
        reward_weight=np.array([1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    ),
    max_episode_steps=20000,
)]
if shaped_reward_envs:
    envs += [dict(
        id=f"MicrortsDefeatRandomEnemyShapedReward-v2",
        entry_point='gym_microrts.envs:GlobalAgentMultiActionsCombinedRewardEnv',
        kwargs=dict(
            frame_skip=0,
            ai2=microrts_ai.randomBiasedAI,
            map_path="maps/10x10/basesWorkers10x10.xml",
            reward_weight=np.array([10.0, 1.0, 1.0, 0.2, 1.0, 4.0, 0.0])
        ),
        max_episode_steps=20000,
    )]

    envs += [dict(
        id=f"MicrortsDefeatWorkerRushEnemyShaped-v2",
        entry_point='gym_microrts.envs:GlobalAgentMultiActionsCombinedRewardEnv',
        kwargs=dict(
            frame_skip=0,
            ai2=microrts_ai.workerRushAI,
            map_path="maps/10x10/basesWorkers10x10.xml",
            reward_weight=np.array([10.0, 1.0, 1.0, 0.2, 1.0, 4.0, 0.0])
        ),
        max_episode_steps=20000,
    )]

    envs += [dict(
        id=f"MicrortsDefeatLightRushEnemyShaped-v2",
        entry_point='gym_microrts.envs:GlobalAgentMultiActionsCombinedRewardEnv',
        kwargs=dict(
            frame_skip=0,
            ai2=microrts_ai.lightRushAI,
            map_path="maps/10x10/basesWorkers10x10.xml",
            reward_weight=np.array([10.0, 1.0, 1.0, 0.2, 1.0, 4.0, 0.0])
        ),
        max_episode_steps=20000,
    )]

    envs += [dict(
        id=f"MicrortsDefeatCoacAIShaped-v2",
        entry_point='gym_microrts.envs:GlobalAgentMultiActionsCombinedRewardEnv',
        kwargs=dict(
            frame_skip=0,
            ai2=microrts_ai.coacAI,
            map_path="maps/10x10/basesWorkers10x10.xml",
            reward_weight=np.array([10.0, 1.0, 1.0, 0.2, 1.0, 4.0, 0.0])
        ),
        max_episode_steps=20000,
    )]

    envs += [dict(
        id=f"MicrortsDefeatNaiveMCTSAIShaped-v2",
        entry_point='gym_microrts.envs:GlobalAgentMultiActionsCombinedRewardEnv',
        kwargs=dict(
            frame_skip=0,
            ai2=microrts_ai.naiveMCTSAI,
            map_path="maps/10x10/basesWorkers10x10.xml",
            reward_weight=np.array([10.0, 1.0, 1.0, 0.2, 1.0, 4.0, 0.0])
        ),
        max_episode_steps=20000,
    )]

if hrl_envs:
    envs += [dict(
        id=f"MicrortsDefeatWorkerRushEnemyHRL-v2",
        entry_point='gym_microrts.envs:GlobalAgentMultiActionsHRLEnv',
        kwargs=dict(
            frame_skip=0,
            ai2=microrts_ai.workerRushAI,
            map_path="maps/10x10/basesWorkers10x10.xml",
            hrl_reward_weights=np.array([
                [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [10.0, 1.0, 1.0, 0.2, 1.0, 4.0, 0.0],
            ])
        ),
        max_episode_steps=20000,
    )]