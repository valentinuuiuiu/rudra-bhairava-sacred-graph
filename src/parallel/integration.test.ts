import TaskDistributor from './taskDistributor';
import agentComm from './agentCommProtocol';

describe('Task Distributor Integration', () => {
  beforeEach(() => {
    // Reset the distributor before each test
    TaskDistributor.getRegisteredAgents().forEach(agent => {
      TaskDistributor.unregisterAgent(agent);
    });
  });

  test('should process valid protocol message', () => {
    const testAgent = 'test-agent-1';
    TaskDistributor.registerAgent(testAgent);

    const testTask = {
      metadata: {
        id: 'task-1',
        project_id: 'project-x',
        workflow_step: 'processing',
        expected_output: 'processed_data',
        payload: { data: 'test' }
      },
      task_type: 'data_processing',
      priority: 'high'
    };

    // Simulate sending a protocol-compliant message
    agentComm.sendMessage({
      from: 'orchestrator',
      to: 'distributor',
      task_type: 'task_submission',
      metadata: {
        project_id: testTask.metadata.project_id,
        workflow_step: testTask.metadata.workflow_step,
        expected_output: testTask.metadata.expected_output
      }
    });

    const result = TaskDistributor.distributeNextTask();
    expect(result.agentId).toBe(testAgent);
    expect(result.task).toEqual(testTask);
  });

  test('should reject invalid protocol message', () => {
    const consoleSpy = jest.spyOn(console, 'error');
    
    // Invalid task missing required fields
    agentComm.sendMessage({
      from: 'orchestrator',
      to: 'distributor',
      task_type: 'task_submission',
      metadata: {
        project_id: 'invalid-project',
        workflow_step: 'invalid-step',
        expected_output: 'invalid-output'
      }
    });

    expect(consoleSpy).toHaveBeenCalled();
    expect(TaskDistributor.getQueueSize()).toBe(0);
  });

  test('should handle round-robin distribution', () => {
    const agents = ['agent-1', 'agent-2', 'agent-3'];
    agents.forEach(agent => TaskDistributor.registerAgent(agent));

    const tasks = [
      {
        metadata: {
          id: 't1',
          project_id: 'p1',
          workflow_step: 's1',
          project_id: 'p1',
          workflow_step: 's1',
          expected_output: 'output1',
          payload: { testData: 'sample' }
        },
        task_type: 't1',
        priority: 'medium',
        payload: { testData: 'sample' }
      },
      {
        metadata: {
          project_id: 'p1',
          workflow_step: 's1',
          expected_output: 'output2',
          payload: { testData: 'sample' }
        },
        task_type: 't2',
        priority: 'medium',
        payload: { testData: 'sample' }
      },
      {
        metadata: {
          project_id: 'p1',
          workflow_step: 's1',
          expected_output: 'output3',
          payload: { testData: 'sample' }
        },
        task_type: 't3',
        priority: 'medium',
        payload: { testData: 'sample' }
      }
    ];

    tasks.forEach(task => TaskDistributor.addTask(task));

    const distributed = tasks.map(() => TaskDistributor.distributeNextTask());
    const agentOrder = distributed.map(d => d.agentId);
    
    // Should distribute in round-robin order
    expect(agentOrder).toEqual(['agent-1', 'agent-2', 'agent-3']);
  });
});