/* RiveScript Playground
 *
 * This code is released under the GNU General Public License version 2.
 */

// The RiveScript bot instance, on the window scope so it can be debugged.
window.rs = null;

$(document).ready(function() {
	// Get all the DOM objects.
	var $form         = $("#playground-form");
	var $btnRun       = $("#run");
	var $btnShare     = $("#share");
	var $btnAbout     = $("#about");
	var $codeEditor   = $("#code");
	var $historyPanel = $("#dialogue");
	var $history      = $("#history");
	var $message      = $("#message");
	var $optDebug     = $("#opt-debug");
	var $optUTF8      = $("#opt-utf8");
	var $optAsync     = $("#opt-async");
	var $debugPanel   = $("#debug-pane");
	var $debugOut     = $("#debug");
	var $rsVersion    = $("#rs-version");

	// Fix disabled states in case of the user reloading the page.
	$codeEditor.prop("disabled", false);
	$message.prop("disabled", true);
	$optUTF8.prop("disabled", false);
	$optAsync.prop("disabled", false);

	// Currently testing the bot?
	var isRunning = false;

	// Populate the RiveScript JS version.
	$rsVersion.text(new RiveScript().version());

	// The about button opens the /about page.
	$btnAbout.on("click", function() {
		window.open("/about");
	});

	// The run button runs the bot.
	$btnRun.on("click", function() {
		var ok = false;
		if (isRunning) {
			ok = teardownBot();
		}
		else {
			ok = initBot();
		}

		if (ok) {
			isRunning = !isRunning;
		}
	});

	// Form submitting and clicking the Send button.
	$form.submit(function() {
		try {
			sendMessage();
		} catch(e) {
			window.alert(e);
		}
		return false;
	})

	// Toggling debug mode.
	$optDebug.on("change", function() {
		if ($optDebug.prop("checked")) {
			$debugPanel.show();
		}
		else {
			$debugPanel.hide();
		}

		// Toggle debugging if the bot is already running.
		if (window.rs !== null) {
			window.rs._debug = true;
		}
	});

	function initBot() {
		// Get their source code.
		var code = $codeEditor.val();
		if (code.length === 0) {
			window.alert("You didn't enter any RiveScript code to run!");
			return false;
		}

		// Update DOM props.
		$btnRun.text("Stop running");
		$codeEditor.prop("disabled", true);
		$optUTF8.prop("disabled", true);
		$optAsync.prop("disabled", true);
		$message.prop("disabled", false);
		$message.focus();

		// Reinitialize the history and debug output.
		$history.empty();
		$debugOut.empty();

		// Initialize the RiveScript bot.
		window.rs = new RiveScript({
			debug: $optDebug.prop("checked"),
			utf8: $optUTF8.prop("checked"),
			onDebug: onDebug
		});
		window.rs.setHandler("coffeescript", new RSCoffeeScript(window.rs));
		window.rs.setHandler("coffee", new RSCoffeeScript(window.rs));
		window.rs.stream(code, function(error) {
			window.alert("Error in your RiveScript code:\n\n" + error);
		});
		window.rs.sortReplies();

		return true;
	};

	function sendMessage() {
		// Get their message.
		var text = $message.val();
		$message.val("");
		if (text.length === 0) {
			return;
		}

		if (window.rs === null) {
			// No bot? Weird.
			window.alert("Weird error: no RiveScript bot is currently active.");
			return;
		}

		// Add the user's message to the history.
		appendHistory("user", text);

		// Get the reply.
		if ($optAsync.prop("checked")) {
			window.rs.replyAsync("web-user", text).then(onReply);
		}
		else {
			var reply = window.rs.reply("web-user", text);
			onReply(reply);
		}
	};

	function onReply(reply) {
		// Add the bot's reply.
		appendHistory("bot", reply);
	};

	function teardownBot() {
		$btnRun.text("Run");
		$codeEditor.prop("disabled", false);
		$message.prop("disabled", true);
		$optUTF8.prop("disabled", false);
		$optAsync.prop("disabled", false);

		window.rs = null;

		return true;
	};

	function onDebug(message) {
		if ($optDebug.prop("checked")) {
			$debugOut.append('<li>' + message + '</li>');
			$debugPanel.scrollTop($debugPanel[0].scrollHeight);
		}
	};

	function appendHistory(className, text) {
		$history.append('<li class="' + className + '">' + text + '</li>');
		$historyPanel.animate({ scrollTop: $historyPanel[0].scrollHeight }, 1000);
	}
});
