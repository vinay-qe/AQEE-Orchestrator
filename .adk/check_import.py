import traceback
try:
    import sys, os
    print('CWD:', os.getcwd())
    print('SYS.PATH:')
    for p in sys.path[:5]:
        print(' -', p)
    print('DIR LIST ROOT:')
    print(os.listdir('.'))
    import qa_orchestrator
    print('MODULE_OK')
    attrs = [a for a in dir(qa_orchestrator) if not a.startswith('__')]
    print('ATTRS:', attrs)
    ra = getattr(qa_orchestrator, 'root_agent', None)
    print('ROOT_AGENT_EXISTS:', ra is not None)
    if ra is not None:
        print('ROOT_AGENT_NAME:', getattr(ra, 'name', None))
except Exception:
    traceback.print_exc()
