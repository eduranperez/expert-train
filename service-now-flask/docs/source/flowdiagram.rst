Slack Bot's flow diagram
=====================================

.. mermaid::

	graph TD;
		A(/GetHelp Can not connect to VPN) --> B(Do any of these help?)
		B --> |Fetch related KB articles| B
		B --> |No| D(Would you like to create a ticket?)
		B --> |Yes| C(Glad to help!)
		D --> |Yes| F(I will first need some contact information.  What is the best email to reach you at?)
		D --> |Not right now| E(Please reach us at XXX or use /GetHelp whenever you need help)
		F --> |email| G(What is the best phone number to reach you at?)
		G --> |xxx-xxx-xxxx| H(What is the prefered method of contact?)
		H --> |email or phone| I(Perfect!  Is Can not connect to VPN an accuret description of the issue?)
		I --> |Yes| J(Your ticket has been submitted!  Someone should be in contact with you shortly.  ETA is X)
		I --> |No| K(Please provide a brief description of the issue)
		K --> |User provides details| J
