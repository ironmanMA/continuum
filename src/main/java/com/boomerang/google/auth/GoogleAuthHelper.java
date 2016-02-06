package com.boomerang.google.auth;

import com.google.api.client.auth.oauth2.Credential;
import com.google.api.client.googleapis.auth.oauth2.GoogleAuthorizationCodeFlow;
import com.google.api.client.googleapis.auth.oauth2.GoogleAuthorizationCodeRequestUrl;
import com.google.api.client.googleapis.auth.oauth2.GoogleTokenResponse;
import com.google.api.client.http.GenericUrl;
import com.google.api.client.http.HttpRequest;
import com.google.api.client.http.HttpRequestFactory;
import com.google.api.client.http.HttpTransport;
import com.google.api.client.http.javanet.NetHttpTransport;
import com.google.api.client.json.JsonFactory;
import com.google.api.client.json.jackson.JacksonFactory;
import java.io.IOException;
import java.security.SecureRandom;
import java.util.Arrays;

//import com.boomerang.config.AppConfigUtil;
import com.boomerang.config.AppConfigLoader;

/**
 * A helper class for Google's OAuth2 authentication API.
 * @version 20140324
 * @author 1. Matyas Danter
 * @author 2. Mohammad
 */
public final class GoogleAuthHelper {


	/**
	 * Please provide a value for the CLIENT_ID constant before proceeding, set this up at https://console.developers.google.com/
	 */
//	private static final String CLIENT_ID = "220984851446-9vs40odb7letnpfakebvpvg4t95jkql8.apps.googleusercontent.com";
	private static final String CLIENT_ID = AppConfigLoader.getValue("google.client.id");
	/**
	 * Please provide a value for the CLIENT_SECRET constant before proceeding, set this up at https://console.developers.google.com/
	 */
//	private static final String CLIENT_SECRET = "sXtWl6YKlH50WPQAEI-YEBmS";
	private static final String CLIENT_SECRET = AppConfigLoader.getValue("google.client.secret");

	/**
	 * Callback URI that google will redirect to after successful authentication
	 */
//	private static final String CALLBACK_URI = "http://localhost/BoomRev/index.jsp";
	private static final String CALLBACK_URI = AppConfigLoader.getValue("google.client.callback.url");

	/**
	 * Callback URI that google will redirect to after successful authentication
	 */
	private static String USER_INFO = "";

	// start google authentication constants
	private static final Iterable<String> SCOPE = Arrays.asList("https://www.googleapis.com/auth/userinfo.profile;https://www.googleapis.com/auth/userinfo.email".split(";"));
	private static final String USER_INFO_URL = "https://www.googleapis.com/oauth2/v1/userinfo";
	private static final JsonFactory JSON_FACTORY = new JacksonFactory();
	private static final HttpTransport HTTP_TRANSPORT = new NetHttpTransport();
	// end google authentication constants

	private String stateToken;
	private String anda;
	private int StateCode = 1;

	private final GoogleAuthorizationCodeFlow flow;

	/**
	 * Constructor initializes the Google Authorization Code Flow with CLIENT ID, SECRET, and SCOPE
	 */
	public GoogleAuthHelper() {
		flow = new GoogleAuthorizationCodeFlow.Builder(HTTP_TRANSPORT,
				JSON_FACTORY, CLIENT_ID, CLIENT_SECRET, SCOPE).build();

		generateStateToken();
	}

	public GoogleAuthHelper( String init) {
		// System.out.println("CLIENT : "+CLIENT_ID+", CLIENT_SECRET : "+CLIENT_SECRET);
		flow = new GoogleAuthorizationCodeFlow.Builder(HTTP_TRANSPORT,
				JSON_FACTORY, CLIENT_ID, CLIENT_SECRET, SCOPE).build();
		System.out.println("AQ"+init);
		anda = init;
	}

	/**
	 * Builds a login URL based on client ID, secret, callback URI, and scope
	 */
	public String buildLoginUrl() {

		final GoogleAuthorizationCodeRequestUrl url = flow.newAuthorizationUrl();
		// System.out.println("[Build Login URL] generated stateToken : "+stateToken);
		return url.setRedirectUri(CALLBACK_URI).setState(stateToken).build();
	}

	/**
	 * Generates a secure state token
	 */
	private void generateStateToken(){
		SecureRandom sr1 = new SecureRandom();
		stateToken = "google;"+sr1.nextInt();
		// System.out.println("[INIT] generated stateToken : "+stateToken);
	}

	/**
	 * Accessor for state token
	 */
	public String getStateToken(){
		System.out.println("[GET TOKEN] generated stateToken : "+stateToken);
		return stateToken;
	}

	/**
	 * Accessor for state token
	 */
	public void printState( String console ){
		System.out.println( "com.boomerang.google.auth.GoogleAuthHelper "+console );
	}

	/**
	 * Publish JSON object to frontend
	 */
	public String getJsonObj(){
		return USER_INFO;
	}

	public int getStateCode(){
		return StateCode;
	}

	public void setStateCode( int setter){
		StateCode = setter;
	}

	/**
	 * Publish JSON object to frontend
	 */
	public void clearJsonObj(){
		USER_INFO = "";
	}

	/**
	 * Check if logged in with boomerangcommerce.com email address
	 */
	public boolean isBoomerangMail(){
		return USER_INFO.contains("@boomerangcommerce.com");
	}

	/**
	 * Expects an Authentication Code, and makes an authenticated request for the user's profile information
	 * @return JSON formatted user profile information
	 * @param authCode authentication code provided by google
	 */
	public String getUserInfoJson(final String authCode) throws IOException {

		final GoogleTokenResponse response = flow.newTokenRequest(authCode).setRedirectUri(CALLBACK_URI).execute();
		final Credential credential = flow.createAndStoreCredential(response, null);
		final HttpRequestFactory requestFactory = HTTP_TRANSPORT.createRequestFactory(credential);
		// Make an authenticated request
		final GenericUrl url = new GenericUrl(USER_INFO_URL);
		final HttpRequest request = requestFactory.buildGetRequest(url);
		request.getHeaders().setContentType("application/json");
		final String jsonIdentity = request.execute().parseAsString();
		USER_INFO = jsonIdentity;
		return jsonIdentity;

	}



}
