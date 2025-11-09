# spacewar

## Protocol

### NewPlayer

```json
    {
      'type': 'newplayer',
      'name': <str>,
      }
```

### Update To Server


```json
    {
      'type': 'move',
      'direction': <AbsoluteRadiansFloat>,
      'location': { 'x': <int>,
                    'y': <int>,
                    },
      'speed': <float>,
      }
 ```

### Update From Server


```json
    {
      '<p1Name>': {
          'direction': <AbsoluteRadiansFloat>,
          'location': { 'x': <int>,
                        'y': <int>,
                        },
      }
 ```
