interface Task {
  metadata: {
    id: string;
    project_id: string;
    workflow_step: string;
  };
  task_type: string;
  priority: 'high'|'medium'|'low';
  payload: any;
  context?: any;
  dependencies?: string[];
  language?: string;
}

class TaskDistributor {
  private agents: string[] = [];
  private currentIndex = 0;
  private taskQueue: Task[] = [];

  registerAgent(agentId: string): void {
    if (!this.agents.includes(agentId)) {
      this.agents.push(agentId);
    }
  }

  unregisterAgent(agentId: string): void {
    this.agents = this.agents.filter(id => id !== agentId);
  }

  addTask(task: Task): void {
    // Validate task structure
    if (!task.metadata || !task.metadata.id || !task.task_type) {
      console.error('Invalid task format:', task);
      return;
    }
    
    this.taskQueue.push(task);
    this.taskQueue.sort((a, b) => {
      if (a.priority === b.priority) return 0;
      if (a.priority === 'high') return -1;
      if (b.priority === 'high') return 1;
      if (a.priority === 'medium') return -1;
      return 1;
    });
    console.log(`Task added: ${task.metadata.id} (${task.task_type})`);
  }

  getNextAgent(): string|null {
    if (this.agents.length === 0) return null;
    
    // Round-robin distribution
    this.currentIndex = (this.currentIndex + 1) % this.agents.length;
    return this.agents[this.currentIndex];
  }

  distributeNextTask(): {agentId: string|null, task: Task|null} {
    if (this.taskQueue.length === 0) return {agentId: null, task: null};
    
    const agentId = this.getNextAgent();
    if (!agentId) return {agentId: null, task: null};

    const task = this.taskQueue.shift()!;
    console.log(`Task distributed: ${task.metadata.id} to agent ${agentId}`);
    return {agentId, task};
  }

  getQueueSize(): number {
    return this.taskQueue.length;
  }

  getRegisteredAgents(): string[] {
    return [...this.agents];
  }
}

export default new TaskDistributor();