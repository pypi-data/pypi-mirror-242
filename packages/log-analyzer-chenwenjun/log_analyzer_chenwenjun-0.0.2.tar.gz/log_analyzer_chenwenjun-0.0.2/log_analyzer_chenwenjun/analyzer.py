from log_analyzer_chenwenjun import logAnalyzer
from log_analyzer_chenwenjun import innerRule

def start(_ruleFile):
    print('------------start---------------')
    logAnalyzer.log_analyze(_ruleFile)


def prepare(eventDict):
    return innerRule.prepare(eventDict)