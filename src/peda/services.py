import asyncio
from peda.base import Event, EventFramework

app = EventFramework()

class UserCreated(Event):
    __topic__ = "users.created"
    user_id: int
    username: str

class SendEmailCommand(Event):
    __topic__ = "emails.send"
    email_address: str
    body: str

@app.subscribe(UserCreated)
async def handle_new_user(event: UserCreated) -> SendEmailCommand:
    print(f"  [Worker: handle_new_user] Processing user: {event.username}")
    
    return SendEmailCommand(
        email_address=f"{event.username}@example.com",
        body="Welcome to the platform!"
    )

@app.subscribe(SendEmailCommand)
async def handle_send_email(event: SendEmailCommand):
    print(f"  [Worker: handle_send_email] Sending email to {event.email_address} with body: '{event.body}'")

async def main():
    await app.start()

    print("\n--- Simulating API Request ---")
    initial_event = UserCreated(user_id=1, username="alice")
    await app.publish(initial_event)

    await asyncio.sleep(0.1) 
    
    print("\n--- Shutting Down ---")
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())