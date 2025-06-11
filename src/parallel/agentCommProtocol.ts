interface AgentMessage {
  from: string;
  to: string;
  task_type: string;
  context: string;
  objective: string;
  requirements: Record<string, any>;
  dependencies: string[];
  priority: 'high'|'medium'|'low';
  deadline?: string;
  language: string;
  metadata: {
    project_id: string;
    workflow_step: string;
    expected_output: string;
  };
}

class AgentCommunication {
  private messageQueue: AgentMessage[] = [];

  sendMessage(message: AgentMessage): void {
    // Validate required fields
    if (!message.from || !message.to || !message.task_type) {
      throw new Error('Invalid message format - missing required fields');
    }
    this.messageQueue.push(message);
  }

  receiveMessage(agentId: string): AgentMessage | null {
    const message = this.messageQueue.find(msg =>
      msg.to === agentId || msg.to === 'broadcast'
    );
    if (message) {
      this.messageQueue = this.messageQueue.filter(msg => msg !== message);
      return message;
    }
    return null;
  }

  broadcast(message: Omit<AgentMessage, 'to'>): void {
    const broadcastMessage: AgentMessage = {
      ...message,
      to: 'broadcast'
    };
    this.sendMessage(broadcastMessage);
  }
}

export default new AgentCommunication();