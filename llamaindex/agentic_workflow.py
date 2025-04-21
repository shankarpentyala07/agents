
from llama_index.core.workflow import StartEvent, StopEvent , Workflow, step
import asyncio

#1.  Basic Workflow Creation
class MyWorkflow(Workflow):
    @step
    async def my_step(self, ev: StartEvent) -> StopEvent:
        # do something here
        return StopEvent(result="Hello, world!")

w = MyWorkflow(timeout=10, verbose=False)
#result = await w.run() 

async def main():
   result = await w.run()
   print(result)

asyncio.run(main())

#2. Connecting Multiple Steps
