interface ResourceMetrics {
  cpu: number;
  memory: number;
  network: number;
}

class AgentHealthMonitor {
  private agents: Map<string, {
    lastHeartbeat: number;
    status: 'active'|'degraded'|'failed';
    resourceUsage: ResourceMetrics;
  }> = new Map();

  registerAgent(agentId: string): void {
    this.agents.set(agentId, {
      lastHeartbeat: Date.now(),
      status: 'active',
      resourceUsage: { cpu: 0, memory: 0, network: 0 }
    });
  }

  updateHeartbeat(agentId: string, resources: ResourceMetrics): void {
    const agent = this.agents.get(agentId);
    if (agent) {
      agent.lastHeartbeat = Date.now();
      agent.resourceUsage = resources;
      agent.status = this.calculateStatus(resources);
    }
  }

  private calculateStatus(resources: ResourceMetrics): 'active'|'degraded'|'failed' {
    if (resources.cpu > 90 || resources.memory > 90) return 'degraded';
    return 'active';
  }

  checkHealth(): { healthy: string[]; degraded: string[]; failed: string[] } {
    const now = Date.now();
    const result: { healthy: string[]; degraded: string[]; failed: string[] } = {
      healthy: [],
      degraded: [],
      failed: []
    };

    this.agents.forEach((agent, agentId) => {
      if (now - agent.lastHeartbeat > 30000) {
        agent.status = 'failed';
      }

      if (agent.status === 'active') result.healthy.push(agentId);
      else if (agent.status === 'degraded') result.degraded.push(agentId);
      else result.failed.push(agentId);
    });

    return result;
  }

  getAgentStatus(agentId: string): string {
    return this.agents.get(agentId)?.status || 'unknown';
  }
}

export default new AgentHealthMonitor();