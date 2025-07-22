import asyncio
import logging
from dotenv import load_dotenv
from livekit.agents.voice import MetricsCollectedEvent
from livekit import rtc
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.plugins import deepgram, elevenlabs, silero, google, noise_cancellation
from livekit.plugins.turn_detector.multilingual import MultilingualModel
from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    JobProcess,
    RoomInputOptions,
    RoomOutputOptions,
    RunContext,
    WorkerOptions,
    cli,
    metrics,
)

from livekit.agents import function_tool

load_dotenv()
logger = logging.getLogger("Job Interview Agent")



class JobInterviwAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="You are a CTO and  job interviewer of a fortune 500 company with over a decade years of experience, you're to interview somoene for a software engineering position. the interview should be professional, engaging and thorough",
        )

    @function_tool
    async def ask_question(self, question: str) -> str:
        """
        Ask a question to the candidate, start the interview with a greeting and introduction.
        """
        logger.info(f"Asking question: {question}")
        return question
    


def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


async def entrypoint(ctx: JobContext):
    ctx.log_context_fields={
        "room_name": ctx.room.name,
    }

    session = AgentSession(
        llm=google.beta.realtime.RealtimeModel(
            model="gemini-2.0-flash-exp",
            voice="Puck",
            temperature=0.8,
            instructions="You are a helpful assistant",
        ),
        stt=deepgram.STT(model="nova-3", language="multi"),
        tts=deepgram.TTS(),
        turn_detection=MultilingualModel(),
        vad=ctx.proc.userdata["vad"],
    )

    usage_collector = metrics.UsageCollector()


    @session.on("metrics_collected")
    def _on_metrics_collected(ev: MetricsCollectedEvent):
        metrics.log_metrics(ev.metrics)
        usage_collector.collect(ev.metrics)

    async def log_usage():
        summary = usage_collector.get_summary()
        logger.info(f"Usage: {summary}")

    # shutdown callbacks are triggered when the session is over
    ctx.add_shutdown_callback(log_usage)

    await session.start(
        agent=JobInterviwAgent(),
        room=ctx.room,
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        ),
        room_output_options=RoomOutputOptions(transcription_enabled=True),
    )

    # joining the room when agent is ready
    await ctx.connect()


