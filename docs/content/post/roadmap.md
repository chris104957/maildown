---
title: "Maildown Roadmap"
description: "Coming to Maildown soon"
draft: false
---

# Roadmap

Maildown is still new and we are adding more functionality all of the 
time. If you have anything else that you'd like to see added to this 
list, please [raise an issue in Github](https://github.com/chris104957/maildown/issues/new?assignees=&labels=&template=feature_request.md&title=)

## More email backends
> [GitHub issue #7](https://github.com/chris104957/maildown/issues/7)

At the moment, Maildown only works on top of Amazon SES. SES is the most
cost-effective email backend available, allowing you to send 52,000
emails per month while remaining in the AWS free tier. However, it comes
with two primary disadvantages:

- Even if you never plan on exceeding these limits, you still need to 
  give Amazon your credit card details
- The onboarding process for SES is somewhat lengthy. After going 
  through the AWS account creation process and adding your billing 
  details, you also need to verify your email addresses, then send a 
  support request to Amazon to take your SES account out of the sandbox.
  
There are a number of other email providers out there with less 
generous limits, but a slightly lower barrier to entry (i.e. just 
simple email ownership verification) and no need to enter any billing
details if you don't plan on exceeding the free limits. Some examples:

- Mailchimp
- SendGrid
- SendInBlue

We'll be looking at adding support for these email providers in the near
future