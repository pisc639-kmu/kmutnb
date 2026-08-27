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

// async function send_webhook(webhookUrl, ip, subpage, hostname) {
async function send_webhook(webhookUrl, embeds) {
  if (!webhookUrl || typeof webhookUrl !== "string" || !webhookUrl.startsWith("https://")) {
    console.error("Invalid or missing DISCORD_WEBHOOK_URL environment variable.");
    return false;
  }

  const embedColor = 5814770; 

  // const safeIp = typeof ip === "string" && ip.trim() ? ip : "Unknown IP";
  // const safeSubpage = typeof subpage === "string" && subpage.trim() ? subpage : "/";
  // const safeHostname = typeof hostname === "string" && hostname.trim() ? hostname : "Unknown Host";

  const payload = {
    username: "Cloudflare Notification",
    avatar_url: "https://dash.cloudflare.com/favicon.ico",
    content: "@everyone Feedback Notification",
    // embeds: [
    //   {
    //     title: "Logger",
    //     color: embedColor,
    //     fields: [
    //       {
    //         name: "IP",
    //         value: safeIp,
    //         inline: true
    //       },
    //       {
    //         name: "URL",
    //         value: safeHostname + safeSubpage,
    //         inline: true
    //       },
    //       {
    //         name: "Host",
    //         value: safeHostname,
    //         inline: false
    //       },
    //       {
    //         name: "Path",
    //         value: safeSubpage,
    //         inline: true
    //       }
    //     ],
    //     footer: {
    //       text: "Edge Runtime Log"
    //     },
    //     timestamp: new Date().toISOString()
    //   }
    // ]
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
      } catch (_) {
        // Fallback if reading the response body fails
      }
      console.error(`Discord API responded with status ${response.status}: ${errorText}`);
      return false;
    }

    return true; 
  } catch (error) {
    console.error("Failed to execute send_webhook due to a network or runtime error:", error);
    return false; 
  }
}

export default {
  async fetch(request, env, ctx) {
    if (request.method === "OPTIONS") {
      return new Response(null, {
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "POST, OPTIONS",
          "Access-Control-Allow-Headers": "Content-Type",
        },
      });
    }

    if (request.method === "POST") {
      try {
        const userIp = request.headers.get('cf-connecting-ip') || 'Unknown IP';
        
        const body = await request.json();
        
        // if (!body || !body.url) {
        //   return new Response(JSON.stringify({ error: "Missing 'url' property in payload" }), { 
        //     status: 400,
        //     headers: { "Content-Type": "application/json" }
        //   });
        // }

        const requiredFields = ['type', 'message', 'contact', 'cf-turnstile-response'];
        const missingField = requiredFields.find(field => !body || !body[field]);

        if (missingField) {
          return new Response(
            JSON.stringify({ error: `Missing required property '${missingField}' in payload` }), 
            { 
              status: 400,
              headers: { "Content-Type": "application/json" }
            }
          );
        }
        
        // cf-turnstile-response
        res = await validateTurnstile(body["cf-turnstile-response"], userIp);
        if (!res.success) {
          return new Response(JSON.stringify({ error: "Turnstile validation failed" }), { 
            status: 400,
            headers: { "Content-Type": "application/json" }
          });
        }

        console.log(`IP: ${userIp} `);
        
        ctx.waitUntil(send_webhook(
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
              footer: {
                text: "Edge Runtime Log"
              },
              timestamp: new Date().toISOString()
            },
            {
              title: "",
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
                  name: "message",
                  value: body.message,
                  inline: true
                }
              ],
              footer: {
                text: "Edge Runtime Log"
              },
              timestamp: new Date().toISOString()
            }
          ]
        ));

        return new Response(JSON.stringify({ success: true }), {
          status: 200,
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
          }
        });
      } catch (err) {
        console.error("Error processing tracking payload:", err);
        return new Response(JSON.stringify({ error: "Invalid tracking payload" }), { 
          status: 400,
          headers: { "Content-Type": "application/json" }
        });
      }
    }

    return new Response("Analytics Server Active", { status: 200 });
  }
};