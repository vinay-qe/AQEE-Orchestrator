#!/usr/bin/env python
"""Test script to verify all agents load correctly."""

import sys
sys.path.insert(0, r'C:\src\qa-agent-ecosystem')

try:
    from agent import root_agent
    print(f'✓ Root agent loaded: {root_agent.name}')
    print(f'✓ Model: {root_agent.model}')
    print(f'✓ Sub-agents count: {len(root_agent.sub_agents)}')
    print(f'✓ Sub-agents:')
    for sub in root_agent.sub_agents:
        print(f'  - {sub.name}')
    print(f'✓ Tools count: {len(root_agent.tools)}')
    print('\n✅ All agents loaded successfully!')
except Exception as e:
    print(f'❌ Error loading agents: {e}')
    import traceback
    traceback.print_exc()
