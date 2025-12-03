/**
 * Supabase Cron Notifications
 * Showcases: Edge Functions + pg_cron
 * Deploy as Supabase Edge Function
 */
import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

serve(async (req) => {
  const supabase = createClient(
    Deno.env.get("SUPABASE_URL")!,
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!
  );

  // Get users who need notifications
  const { data: users } = await supabase
    .from("users")
    .select("id, email, preferences")
    .eq("notifications_enabled", true);

  // Send notifications (mock - replace with real email service)
  const notifications = users?.map(user => ({
    user_id: user.id,
    message: `Daily update for ${user.email}`,
    sent_at: new Date().toISOString()
  })) || [];

  // Log notifications
  await supabase.from("notification_log").insert(notifications);

  return new Response(
    JSON.stringify({ sent: notifications.length }),
    { headers: { "Content-Type": "application/json" } }
  );
});

// SQL to set up cron job (run in Supabase SQL editor):
/*
SELECT cron.schedule(
  'daily-notifications',
  '0 9 * * *',  -- Every day at 9 AM
  $$
  SELECT net.http_post(
    url := 'https://your-project.supabase.co/functions/v1/notifications',
    headers := '{"Authorization": "Bearer YOUR_ANON_KEY"}'::jsonb
  );
  $$
);
*/
