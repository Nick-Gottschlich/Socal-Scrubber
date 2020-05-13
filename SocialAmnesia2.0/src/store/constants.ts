// ACTIONS TO MODIFY VALUES IN STATE
const LOGIN_TO_TWITTER = "logIntoTwitter";
const UPDATE_TWITTER_SCREEN_NAME = "updateTwitterScreenName";
const UPDATE_TWITTER_USER_ID = "updateTwitterUserId";
const UPDATE_USER_TWEETS = "updateUserTweets";
const UPDATE_USER_FAVORITES = "updateUserFavorites";
const UPDATE_TWITTER_USER_KEYS = "updateTwitterUserKeys";
const UPDATE_USER_CLIENT = "updateUserClient";
const UPDATE_WHITELISTED_TWEETS = "updateWhitelistedTweets";
const UPDATE_WHITELISTED_FAVORITES = "updateWhitelistedFavorites";
const INCREMENT_CURRENTLY_DELETING_ITEMS_DELETED =
  "incrementCurrentlyDeletingItemsDeleted";
const RESET_CURRENTLY_DELETING_ITEMS_DELETED =
  "resetCurrentlyDeletingItemsDeleted";
const UPDATE_CURRENTLY_DELETING_TOTAL_ITEMS =
  "updateCurrentlyDeletingTotalTweets";

// ACTUAL VALUES IN STATE
const TWITTER_LOGGED_IN = "twitterLoggedIn";
const TWITTER_SCREEN_NAME = "twitterScreenName";
const TWITTER_USER_ID = "twitterUserId";
const USER_TWEETS = "userTweets";
const USER_FAVORITES = "userFavorites";
const TWITTER_USER_KEYS = "twitterUserKeys";
const TWITTER_USER_CLIENT = "twitterUserClient";
const WHITELISTED_TWEETS = "whitelistedTweets";
const WHITELISTED_FAVORITES = "whitelistedFavorites";
const CURRENTLY_DELETING = "currentlyDeleting";

// other constants
const TWEETS_ROUTE = "statuses/user_timeline";
const FAVORITES_ROUTE = "favorites/list";

const constants = {
  LOGIN_TO_TWITTER,
  UPDATE_TWITTER_SCREEN_NAME,
  UPDATE_TWITTER_USER_ID,
  UPDATE_USER_TWEETS,
  UPDATE_USER_FAVORITES,
  UPDATE_TWITTER_USER_KEYS,
  UPDATE_USER_CLIENT,
  UPDATE_WHITELISTED_TWEETS,
  UPDATE_WHITELISTED_FAVORITES,
  INCREMENT_CURRENTLY_DELETING_ITEMS_DELETED,
  RESET_CURRENTLY_DELETING_ITEMS_DELETED,
  UPDATE_CURRENTLY_DELETING_TOTAL_ITEMS,
  TWITTER_LOGGED_IN,
  TWITTER_SCREEN_NAME,
  TWITTER_USER_ID,
  USER_TWEETS,
  USER_FAVORITES,
  TWITTER_USER_KEYS,
  TWITTER_USER_CLIENT,
  WHITELISTED_TWEETS,
  WHITELISTED_FAVORITES,
  CURRENTLY_DELETING,
  TWEETS_ROUTE,
  FAVORITES_ROUTE
};

export default constants;