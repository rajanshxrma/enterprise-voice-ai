import json
import openai
from config import settings
from database import SessionLocal, CallRecord, Transcript, CallOutcome, CallStatus
from services.prompts import ROUTER_PROMPT, SALES_AGENT_PROMPT, CLAIMS_AGENT_PROMPT

client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

class AgentRouter:
    def __init__(self, call_sid: str):
        self.call_sid = call_sid
        self.current_mode = "router" # router, sales, claims
        self.conversation_history = []
        
        # add initial system prompt
        self.conversation_history.append({"role": "system", "content": ROUTER_PROMPT})
        
    async def process_user_message(self, text: str) -> dict:
        """
        Takes the transcribed text from the user, feeds it to the LLM,
        and returns the AI's response text and any triggers.
        """
        # save transcript to db
        self._log_transcript("user", text)
        
        self.conversation_history.append({"role": "user", "content": text})
        
        # force JSON object response format via OpenAI API
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=self.conversation_history,
            response_format={"type": "json_object"},
            temperature=0.7
        )
        
        try:
            ai_data = json.loads(response.choices[0].message.content)
        except Exception as e:
            ai_data = {"message": "I'm having a little trouble understanding, could you repeat that?", "trigger": "none", "route": "none"}
            
        ai_message = ai_data.get("message", "")
        route = ai_data.get("route", "none")
        trigger = ai_data.get("trigger", "none")
        
        # log ai transcript
        self._log_transcript("agent", ai_message)
        self.conversation_history.append({"role": "assistant", "content": json.dumps(ai_data)})
        
        # handle routing logic
        if self.current_mode == "router" and route in ["sales", "claims"]:
            self.current_mode = route
            self._update_call_record_agent(route)
            # swap the system prompt by replacing the first message
            if route == "sales":
                self.conversation_history[0] = {"role": "system", "content": SALES_AGENT_PROMPT}
            else:
                self.conversation_history[0] = {"role": "system", "content": CLAIMS_AGENT_PROMPT}
                
            # FORCE GENERATE THE NEW AGENT'S GREETING
            self.conversation_history.append({"role": "system", "content": "You were just connected to the user. Introduce yourself and ask how you can help."})
            
            response2 = await client.chat.completions.create(
                model="gpt-4o",
                messages=self.conversation_history,
                response_format={"type": "json_object"},
                temperature=0.7
            )
            try:
                ai_data2 = json.loads(response2.choices[0].message.content)
            except Exception:
                ai_data2 = {"message": "Hi, how can I help you?", "trigger": "none"}
                
            # Combine the router's connection message with the new agent's greeting
            ai_message += " ... " + ai_data2.get("message", "")
            
            # Remove the temporary system prompt and append the real assistant message
            self.conversation_history.pop()
            self.conversation_history.append({"role": "assistant", "content": json.dumps(ai_data2)})

        # handle triggers (end call / escalate)
        outcome_mapping = {
            "payment": CallOutcome.SALE_CLOSED,
            "rejected": CallOutcome.REJECTED_OTHER,
            "escalate_legal_risk": CallOutcome.ESCALATED_LEGAL_RISK,
            "escalate_human": CallOutcome.ESCALATED_HUMAN
        }
        
        is_call_over = False
        if trigger in outcome_mapping:
            self._update_call_outcome(outcome_mapping[trigger])
            is_call_over = True
            
        return {
            "text": ai_message,
            "is_call_over": is_call_over,
            "current_mode": self.current_mode
        }
        
    def _log_transcript(self, speaker: str, text: str):
        db = SessionLocal()
        try:
            record = db.query(CallRecord).filter(CallRecord.twilio_call_sid == self.call_sid).first()
            if record:
                transcript = Transcript(call_id=record.id, speaker=speaker, text=text)
                db.add(transcript)
                db.commit()
        except Exception as e:
            print(f"db error logging transcript: {e}")
        finally:
            db.close()
            
    def _update_call_record_agent(self, agent_type: str):
        db = SessionLocal()
        try:
            record = db.query(CallRecord).filter(CallRecord.twilio_call_sid == self.call_sid).first()
            if record:
                record.agent_type = agent_type
                db.commit()
        finally:
            db.close()
            
    def _update_call_outcome(self, outcome: CallOutcome):
        db = SessionLocal()
        try:
            record = db.query(CallRecord).filter(CallRecord.twilio_call_sid == self.call_sid).first()
            if record:
                record.outcome = outcome
                record.status = CallStatus.COMPLETED
                db.commit()
        finally:
            db.close()
