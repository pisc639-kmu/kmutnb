const SECRET_KEY = "0x4AAAAAAEdwIDgNVObM3tshIMJHkzNs1uY";

async function validateTurnstile(token, remoteip) {
  try {
    const response = await fetch(
      "https://challenges.cloudflare.com/turnstile/v0/siteverify",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          secret: SECRET_KEY,
          response: token,
          remoteip: remoteip,
        }),
      },
    );

    const result = await response.json();
    return result;
  } catch (error) {
    console.error("Turnstile validation error:", error);
    return { success: false, "error-codes": ["internal-error"] };
  }
}

async function send_webhook(webhookUrl, embeds) {
  if (!webhookUrl || typeof webhookUrl !== "string" || !webhookUrl.startsWith("https://")) {
    console.error("Invalid or missing DISCORD_WEBHOOK_URL environment variable.");
    return false;
  }

  const payload = {
    username: "Cloudflare Notification",
    avatar_url: "https://dash.cloudflare.com/favicon.ico",
    content: "@everyone Feedback Notification",
    embeds: embeds
  };

  try {
    const response = await fetch(webhookUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      let errorText = "Unknown error";
      try {
        errorText = await response.text();
      } catch (_) {}
      console.error(`Discord API responded with status ${response.status}: ${errorText}`);
      return false;
    }

    return true; 
  } catch (error) {
    console.error("Failed to execute send_webhook due to a network or runtime error:", error);
    return false; 
  }
}

// Cloudflare Pages Functions specific routing handler for POST requests
export async function onRequestPost(context) {
  const { request, waitUntil } = context;
  const embedColor = 5814770; 

  // Handle CORS Preflight / Simple Responses if needed
  const corsHeaders = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
  };

  try {
    const userIp = request.headers.get('cf-connecting-ip') || 'Unknown IP';
    const body = await request.json();
    
    // Check required fields
    const requiredFields = ['type', 'message', 'contact', 'cf-turnstile-response'];
    const missingField = requiredFields.find(field => !body || !body[field]);

    if (missingField) {
      return new Response(
        JSON.stringify({ error: `Missing required property '${missingField}' in payload` }), 
        { status: 400, headers: corsHeaders }
      );
    }
    
    // FIX: Added 'const' to 'res' to prevent "ReferenceError: res is not defined"
    const res = await validateTurnstile(body["cf-turnstile-response"], userIp);
    if (!res.success) {
      return new Response(JSON.stringify({ error: "Turnstile validation failed" }), { 
        status: 400, 
        headers: corsHeaders 
      });
    }

    console.log(`IP: ${userIp} `);
    
    // FIX: Using Cloudflare Pages context 'waitUntil' syntax
    waitUntil(send_webhook(
      "https://discord.com/api/webhooks/1542584397881020487/oKv7kgueS_dFBh4tu-n8QEB2X5MZN1N9SWyaZW70lgAmLAjGN0-9hWI__z28tZXovci5",
      [
        {
          title: "Sender Info",
          color: embedColor,
          fields: [
            {
              name: "IP",
              value: userIp,
              inline: true
            }
          ],
          footer: { text: "Edge Runtime Log" },
          timestamp: new Date().toISOString()
        },
        {
          title: "Feedback Details",
          color: embedColor,
          fields: [
            {
              name: "Contact",
              value: body.contact,
              inline: true
            },
            {
              name: "Type",
              value: body.type,
              inline: true
            },
            {
              name: "Message",
              value: body.message,
              inline: false // Changed to false so message text spans full width
            }
          ],
          footer: { text: "Edge Runtime Log" },
          timestamp: new Date().toISOString()
        }
      ]
    ));

    return new Response(JSON.stringify({ success: true }), {
      status: 200,
      headers: corsHeaders
    });
  } catch (err) {
    console.error("Error processing tracking payload:", err);
    return new Response(JSON.stringify({ error: "Invalid tracking payload" }), { 
      status: 400,
      headers: corsHeaders
    });
  }
}

// Optional: Handle OPTIONS preflight requests smoothly at this route
export async function onRequestOptions() {
  return new Response(null, {
    status: 204,
    headers: {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    }
  });
}
