package com.boomerang.config;

/**
 * @author prateek sachdeva, abhi, mohammad arafath
 */

import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.Properties;

import org.apache.commons.configuration.Configuration;
import org.apache.commons.configuration.ConfigurationException;
import org.apache.commons.configuration.PropertiesConfiguration;
import org.apache.commons.lang3.StringUtils;
import org.json.JSONObject;

import com.boomerang.config.AppConfigConstants;

public class AppConfigLoader {

	private static Properties configProperties = null;
	private static Configuration prefixProperties = null;
	private static ArrayList <String> ConfigPathsApps = new ArrayList <String> ();

	public static void loadConfigs(ArrayList <String> appConfigPaths){
		InputStream input = null;
		configProperties = new Properties();
		for (int i=0; i<appConfigPaths.size(); i++) {
			try {
				input = new FileInputStream(appConfigPaths.get(i));

				Properties newProperty = new Properties();
				newProperty.load( new FileInputStream( appConfigPaths.get(i)));
				configProperties.putAll(newProperty);

				ConfigPathsApps.add(i, appConfigPaths.get(i));

			} catch (IOException ex) {
				ex.printStackTrace();
			} finally {
			if (input != null) {
					try {
						input.close();
					} catch (IOException e) {
						e.printStackTrace();
					}
				}
			}
		}

	}

	public static String getValue(String key) {
		if(configProperties != null && key != null){
			return configProperties.getProperty(key);
		}
		return "";
	}

	public static String getUIConfigValues() {
		try{
			prefixProperties = new PropertiesConfiguration(ConfigPathsApps.get(0));
		} catch (ConfigurationException e) {
			e.printStackTrace();
		}

		JSONObject config = new JSONObject();
		for(String prefix:AppConfigConstants.PREFIXES){
			config.put(prefix, getNestedPropertiesAsJson(prefix));
		}
		return config.toString();
	}

	public static String getHASHConfigValues() {
		try{
			prefixProperties = new PropertiesConfiguration(ConfigPathsApps.get(1));
		} catch (ConfigurationException e) {
			e.printStackTrace();
		}

		JSONObject config = new JSONObject();
		for(String prefix:AppConfigConstants.HASH_PREFIXES){
			config.put(prefix, getNestedPropertiesAsJson(prefix));
		}
		return config.toString();
	}

	public static JSONObject getNestedPropertiesAsJson(String prefix){
		JSONObject jsonObj = new JSONObject();
		Iterator<String> prefixKeys = prefixProperties.getKeys(prefix);
		while (prefixKeys.hasNext()) {
			String prefixKey = prefixKeys.next();
			String key = null;
			if(prefix.equalsIgnoreCase(prefixKey)){
				key = StringUtils.substringAfter(prefixKey,AppConfigConstants.DELIMITER).trim();
			}
			else{
				key = prefixKey.replace(prefix + AppConfigConstants.DELIMITER, AppConfigConstants.BLANK).trim();
			}
			Object value = (Object) prefixProperties.getProperty(prefixKey);
			if(key.contains(AppConfigConstants.DELIMITER)){
				String nestedKey = StringUtils.substringBefore(key,AppConfigConstants.DELIMITER);
				jsonObj.put(nestedKey,getNestedPropertiesAsJson(prefix+AppConfigConstants.DELIMITER+nestedKey));
			}
			else{
				jsonObj.put(key, value);
			}

		}
		return jsonObj;
	}

}
