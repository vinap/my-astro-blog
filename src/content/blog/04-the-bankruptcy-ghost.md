---
title: 'The Bankruptcy Ghost: The Liability Chain'
description: 'Executing a $1M PO for a customer that no longer exists.'
pubDate: '2027-04-19'
heroImage: '../../assets/images/blog/04-the-bankruptcy-ghost.png'
---

Procurement systems are very good at validating fields. They are much worse at understanding context. That is how you end up with a legally valid purchase order tied to a commercially dead opportunity.

I call this the **Bankruptcy Ghost**.

The ghost appears when your workflow is technically flawless but strategically blind. The cart is approved. The supplier is active. The contract reference exists. The PO transmits successfully. Every checkbox is green. Then the outside world changes overnight and your perfect process turns into an expensive mistake.

**The Scenario That Still Sticks With Me:**
We were dealing with custom-tooled components for a customer-specific product line. Nothing about the buy was reusable. Once the supplier started, the material and tooling were effectively married to that one commercial program.

On Friday evening, everyone felt efficient. Procurement had moved quickly. The supplier had acknowledged. Internal teams were happy that the process had flowed without delay.

By Saturday morning, the customer filed for Chapter 11.

That was the moment when "operational excellence" became a liability chain.

**Why Systems Miss This:**
Most legacy procurement platforms make decisions using internal truth only:

- Is the supplier approved?
- Is budget available?
- Is the requester authorized?
- Is the spend within policy?

Those are necessary controls, but they are not enough for high-risk buys. If you are procuring customer-specific material, tooling, long-lead components, or custom packaging, external commercial health matters just as much as internal approval.

I have seen teams deploy elegant workflows that never once ask the question a seasoned sourcing manager would ask instinctively: "Has anything changed about the commercial viability of this customer since this requisition was created?"

**How The Failure Unfolds In Software:**
The dangerous point is usually after approval but before commitment, or immediately after transmission when the supplier begins work. Legacy systems do not have a contextual kill switch. They move linearly. Once the state changes to sent, downstream actions fire:

- internal PO cascades
- supplier scheduling
- material reservation
- tooling preparation
- freight planning

The system assumes continuity because the workflow engine has no awareness of credit distress, bankruptcy news, or sudden risk spikes.

**A Human Version Of The Problem:**
Imagine being the buyer on Monday morning. Sales says the customer situation is "under review". Finance says legal is checking exposure. The supplier says production already started because the PO was released on Friday. You now own a conversation nobody wanted to have: can we stop? how much is cancelable? what is already committed? who approved without knowing? what can be repurposed?

This is where software design becomes very real. If the platform cannot trace commitment stage, cancellation windows, and customer-risk context, then the business is negotiating blind after the fact.

**What Better Looks Like:**
For customer-specific spend, a smarter system should treat external risk signals as first-class inputs. Before release, and again before supplier commitment, it should re-evaluate:

- customer credit health
- major adverse news
- program viability
- cancellation terms
- amount of non-recoverable exposure

Then it should tell the buyer, in plain language, "This order is legally ready but commercially risky. Expected non-cancelable exposure: $1.2M."

That single sentence would save companies more money than many dashboard programs I have seen funded.

**Where Experience Changes Your View:**
After years in procurement software, I no longer believe process speed alone is always good. Speed without context is just faster commitment to bad information. Mature sourcing organizations know the difference between friction and judgment. Good software should reduce the first and amplify the second.

**The Final Insight:**
Procurement does not happen in a vacuum. A PO is not just a transaction. It is a commitment inside a living commercial environment. If your platform cannot sense when that environment has changed, then your controls are incomplete, no matter how polished the workflow looks in the demo.
