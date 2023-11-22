from log-analyzer-cwj import logAnalyzer
from log-analyzer-cwj import innerRule

def start(_ruleFile):
    print('------------start---------------')
    logAnalyzer.log_analyze(_ruleFile)


def prepare(eventDict):
    return innerRule.prepare(eventDict)